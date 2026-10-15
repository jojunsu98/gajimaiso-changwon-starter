"""가지마이소창원: KOSIS DT_1B26001_A01 원본 CSV의 기초 검수와 월별 정제.

Python 3.10+ 표준 라이브러리만 사용한다. 원본 파일은 수정하지 않는다.
이 스크립트는 코드가 포함된 2줄 머리글/지역별 행 형식의 CSV에 맞춰 작성했다.
실행 예:
  python prepare_data.py "시군구별_이동자수_20261015174157.csv"

출처: https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1B26001_A01
통계표 메타자료: 2010-07-01 통합 창원시 신설; 창원의 일반구는 별도 집계 단위에서 제외.
단위: 명. external_inflow/outflow는 총전입/총전출에서 시군구내 이동을 뺀 값이다.
이상치 삭제, 보간, 예측, 인과 해석은 수행하지 않는다.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from pathlib import Path

ITEMS = {
    "T10": "total_inflow",             # 총전입: 창원시 내부 이동 포함
    "T20": "total_outflow",            # 총전출: 창원시 내부 이동 포함
    "T25": "net_migration",            # 순이동: 전입 - 전출
    "T30": "within_city_movement",     # 시도내이동-시군구내
    "T31": "within_province_inflow",   # 경남 내 다른 시군 → 창원
    "T32": "within_province_outflow",  # 창원 → 경남 내 다른 시군
    "T40": "interprovince_inflow",     # 다른 시도 → 창원
    "T50": "interprovince_outflow",    # 창원 → 다른 시도
}
REGION_CODE = "48120"


def load_csv(path: Path) -> tuple[list[list[str]], str]:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "cp949"):
        try:
            text = raw.decode(encoding)
            return list(csv.reader(io.StringIO(text))), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError("UTF-8 또는 CP949로 읽을 수 없는 파일입니다.")


def prepare(source: Path, output: Path) -> dict:
    if source.resolve() == output.resolve():
        raise ValueError("원본 파일을 덮어쓸 수 없습니다. 출력 파일명을 다르게 지정하세요.")
    rows, encoding = load_csv(source)
    if len(rows) < 3 or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("2줄 머리글과 지역별 데이터 행의 열 개수를 확인하세요.")
    selected = [row for row in rows[2:] if row and row[0].split()[0] == REGION_CODE]
    if len(selected) != 1:
        raise ValueError(f"{REGION_CODE} 창원시 행이 정확히 1개 있어야 합니다.")

    by_month: dict[str, dict[str, int]] = {}
    selected_row = selected[0]
    for index in range(1, len(rows[0])):
        month_match = re.fullmatch(r"M(\d{4})(\d{2})\s+(\d{4})\.(\d{2})", rows[0][index].strip())
        if not month_match:
            raise ValueError(f"시점 머리글 형식을 확인하세요: {rows[0][index]!r}")
        year, month, display_year, display_month = month_match.groups()
        if (year, month) != (display_year, display_month) or not 1 <= int(month) <= 12:
            raise ValueError("시점 코드와 표시 날짜가 일치하지 않거나 월이 잘못되었습니다.")
        key = f"{year}-{month}"
        item_code = rows[1][index].split()[0]
        if item_code not in ITEMS:
            raise ValueError(f"예상하지 않은 항목 코드: {item_code}")
        bucket = by_month.setdefault(key, {})
        if item_code in bucket:
            raise ValueError(f"중복된 월-항목: {key}/{item_code}")
        raw_value = selected_row[index].strip().replace(",", "")
        if not re.fullmatch(r"[+-]?\d+", raw_value):
            raise ValueError(f"결측/비수치 값을 임의로 보정하지 않습니다: {key}/{item_code}={raw_value!r}")
        value = int(raw_value)
        if item_code != "T25" and value < 0:
            raise ValueError(f"인원수에 음수가 있습니다: {key}/{item_code}")
        bucket[item_code] = value

    months = sorted(by_month)
    if not months:
        raise ValueError("유효한 월별 자료가 없습니다.")
    serials = [int(m[:4]) * 12 + int(m[5:]) - 1 for m in months]
    if serials != list(range(serials[0], serials[-1] + 1)):
        raise ValueError("중간에 빠진 월이 있습니다.")
    if months[0] < "2010-07":
        raise ValueError("통합 창원시 출범 전 시점은 이 정제 기준으로 분석하지 않습니다.")

    clean_rows: list[dict] = []
    for month in months:
        x = by_month[month]
        if set(x) != set(ITEMS):
            raise ValueError(f"필수 8개 항목이 모두 있지 않습니다: {month}")
        checks = {
            "총전입-총전출=순이동": x["T10"] - x["T20"] == x["T25"],
            "총전입=시군구내+시군구간전입+시도간전입": x["T10"] == x["T30"] + x["T31"] + x["T40"],
            "총전출=시군구내+시군구간전출+시도간전출": x["T20"] == x["T30"] + x["T32"] + x["T50"],
        }
        failed = [name for name, passed in checks.items() if not passed]
        if failed:
            raise ValueError(f"{month} 집계 불일치: {failed}")
        external_inflow = x["T31"] + x["T40"]
        external_outflow = x["T32"] + x["T50"]
        if external_inflow - external_outflow != x["T25"]:
            raise ValueError(f"{month} 창원 경계 이동의 순이동 불일치")
        clean_rows.append({
            "month": month, "region_code": REGION_CODE, "region_name": "창원시",
            **{name: x[code] for code, name in ITEMS.items()},
            "external_inflow": external_inflow,
            "external_outflow": external_outflow,
        })

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(clean_rows[0]))
        writer.writeheader()
        writer.writerows(clean_rows)
    return {
        "source": source.name,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "encoding": encoding,
        "selected_region": selected_row[0],
        "excluded_region_rows": [row[0] for row in rows[2:] if row is not selected_row],
        "first_month": months[0], "last_month": months[-1], "months": len(months),
        "raw_numeric_cells": len(months) * len(ITEMS),
        "missing_months": 0, "duplicate_month_item_pairs": 0,
        "missing_or_nonnumeric_values": 0,
        "checks_passed_per_month": 4, "months_passing_checks": len(months),
        "imputation_applied": False, "outlier_deletion_applied": False,
        "outlier_assessment": "not_performed",
        "output": str(output), "output_rows": len(clean_rows),
        "output_columns": len(clean_rows[0]),
        "first_row": clean_rows[0], "last_row": clean_rows[-1],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="KOSIS에서 받은 코드 포함 원본 CSV")
    parser.add_argument("--output", type=Path, default=Path("changwon_migration_monthly_clean.csv"))
    args = parser.parse_args()
    try:
        result = prepare(args.source, args.output)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"정제 중단: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
