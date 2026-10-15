"""가지마이소창원: 원본 검증 → 정제 → 기초 시계열 그래프 3개.

실행: python analysis.py
원본(data/raw)은 수정하지 않는다. 실행 시 data의 정제본과 images/results를 갱신한다.
파일 기준 경로를 사용하므로 다른 작업 디렉터리에서 실행해도 작동한다.
AI 생성 보조 코드. 분석 원인·서비스 효과·최종 결론을 자동으로 작성하지 않는다.
"""
from __future__ import annotations

import csv
import json
import math
import platform
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from statistics import mean

try:
    import matplotlib
except ImportError as error:
    raise SystemExit("Matplotlib가 없습니다. 먼저 requirements.txt를 설치하세요.") from error

# 별도 창이나 웹서버 대신 PNG를 저장한다.
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import StrMethodFormatter

from prepare_data import ITEMS, prepare

ROOT = Path(__file__).resolve().parent
WINDOW = 12
METRICS = ("external_inflow", "external_outflow", "net_migration")


def choose_font() -> bool:
    """설치된 글꼴만 사용한다. 한글 글꼴이 없으면 영문 표기로 전환한다."""
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in ("Malgun Gothic", "AppleGothic", "NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP"):
        if candidate in available:
            plt.rcParams["font.family"] = candidate
            plt.rcParams["axes.unicode_minus"] = False
            return True
    return False


def moving_average(values: list[int], window: int = WINDOW) -> list[float]:
    """당월과 직전 11개월의 평균. 12개월 미만인 첫 11개 시점은 NaN."""
    if window < 1:
        raise ValueError("이동평균 창은 1 이상이어야 합니다.")
    return [math.nan if i + 1 < window else mean(values[i + 1 - window:i + 1]) for i in range(len(values))]


def read_clean(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 100:
        raise ValueError("100개월 이상의 데이터가 필요합니다.")
    fields = list(ITEMS.values()) + ["external_inflow", "external_outflow"]
    for row in rows:
        row["date"] = datetime.strptime(row["month"], "%Y-%m")
        for field in fields:
            row[field] = int(row[field])
    return rows


def monthly_pattern(rows: list[dict]) -> tuple[list[dict], list[int]]:
    """12개월이 모두 존재하는 연도만 사용하여 월별 평균을 계산한다."""
    by_year = defaultdict(list)
    for row in rows:
        by_year[row["date"].year].append(row)
    years = sorted(y for y, group in by_year.items() if {r["date"].month for r in group} == set(range(1, 13)))
    if not years:
        raise ValueError("월별 평균 비교에 사용할 완결 연도가 없습니다.")
    output = []
    for month in range(1, 13):
        group = [r for y in years for r in by_year[y] if r["date"].month == month]
        output.append({
            "calendar_month": month, "n_years": len(group),
            **{f"mean_{metric}": mean([r[metric] for r in group]) for metric in METRICS},
        })
    return output, years


def save_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    raw = ROOT / "data" / "raw" / "migration_raw.csv"
    clean = ROOT / "data" / "changwon_migration_monthly_clean.csv"
    images = ROOT / "images"
    results = ROOT / "results"
    if not raw.is_file():
        raise FileNotFoundError(f"원본이 없습니다: {raw}")
    images.mkdir(exist_ok=True)
    results.mkdir(exist_ok=True)

    # 이전 정제 코드를 그대로 호출하여 지역코드, 결측, 중복, 집계식을 재검증한다.
    validation = prepare(raw, clean)
    rows = read_clean(clean)
    patterns, complete_years = monthly_pattern(rows)
    moving = {metric: moving_average([r[metric] for r in rows]) for metric in METRICS}
    dates = [r["date"] for r in rows]
    period = f"{rows[0]['month']} ~ {rows[-1]['month']}"
    ko = choose_font()

    def text(korean: str, english: str) -> str:
        return korean if ko else english

    def new_chart(title: str, subtitle: str):
        fig = plt.figure(figsize=(12, 6.3), dpi=160)
        ax = fig.add_axes([0.10, 0.19, 0.86, 0.63])
        fig.text(0.10, 0.94, title, fontsize=18, weight="bold", va="top")
        fig.text(0.10, 0.87, subtitle, fontsize=10, va="top")
        ax.grid(axis="y", alpha=0.25)
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        return fig, ax

    def date_axis(ax):
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.set_xlim(dates[0] - timedelta(days=16), dates[-1] + timedelta(days=16))
        ax.set_xlabel(text("시점", "Month"))

    def finish(fig, filename: str, note: str):
        fig.text(0.10, 0.090, note, fontsize=9, va="top")
        fig.text(0.10, 0.048, text("출처: KOSIS 국내인구이동통계 DT_1B26001_A01 | 지역코드 48120 | 내려받은 자료 기준", "Source: KOSIS DT_1B26001_A01 | Region 48120 | Uploaded data snapshot"), fontsize=8, va="top")
        fig.savefig(images / filename, dpi=160)
        plt.close(fig)

    # 1. 원시 월별 값과 후행 이동평균. 미래 자료나 보간값은 사용하지 않는다.
    fig, ax = new_chart(text("가지마이소창원 | 외부 전입·전출 추세", "Changwon | External inflow and outflow"),
                        text(f"{period} · 창원 내부 이동 제외 · 얇은 선: 월별 수치 / 굵은 선: 12개월 평균", f"{period} | Internal moves excluded | Monthly values and trailing 12-month means"))
    ax.plot(dates, [r["external_inflow"] for r in rows], linewidth=1.0, alpha=0.6, label=text("외부 전입 월별", "External inflow / monthly"))
    ax.plot(dates, [r["external_outflow"] for r in rows], linewidth=1.0, alpha=0.6, label=text("외부 전출 월별", "External outflow / monthly"))
    ax.plot(dates, moving["external_inflow"], linewidth=2.5, label=text("외부 전입 12개월 평균", "Inflow / 12-month mean"))
    ax.plot(dates, moving["external_outflow"], linewidth=2.5, linestyle="--", label=text("외부 전출 12개월 평균", "Outflow / 12-month mean"))
    ax.set_ylabel(text("월 이동자수 (명)", "Movers per month"))
    ax.set_ylim(0, max(max(r["external_inflow"], r["external_outflow"]) for r in rows) * 1.25)
    date_axis(ax)
    ax.legend(loc="upper right", fontsize=9, ncol=2)
    finish(fig, "01_external_trend.png", text("12개월 평균 = 당월과 직전 11개월의 평균. 첫 11개월의 평균은 계산하지 않음.", "Trailing mean uses the current and previous 11 months; the first 11 means are not calculated."))

    # 2. 0선 아래는 순유출. 순이동은 전체 인구 증감과 같은 개념이 아니다.
    fig, ax = new_chart(text("가지마이소창원 | 월별 순이동", "Changwon | Monthly net migration"),
                        text(f"{period} · 순이동 = 외부 전입 - 외부 전출", f"{period} | Net migration = external inflow - external outflow"))
    ax.bar(dates, [r["net_migration"] for r in rows], width=22, label=text("월별 순이동", "Monthly net migration"))
    ax.axhline(0, linewidth=1)
    ax.set_ylabel(text("순이동 (명)", "Net movers"))
    date_axis(ax)
    finish(fig, "02_net_migration.png", text("0보다 작으면 순유출, 크면 순유입. 출생·사망 등은 포함하지 않은 이동에 따른 차이.", "Below zero: net outflow. Above zero: net inflow. This is not total population change."))

    # 3. 부분 연도인 2026년은 배제: 각 월에 동일한 10개 연도가 기여한다.
    years_label = f"{complete_years[0]}~{complete_years[-1]}"
    fig, ax = new_chart(text("가지마이소창원 | 달에 따라 이동 규모가 다를까?", "Changwon | Average moves by calendar month"),
                        text(f"{years_label} 완결 연도만 사용 · 각 월 {len(complete_years)}개 연도 평균 · 부분 연도 제외", f"Complete years only: {years_label} | {len(complete_years)} observations per calendar month"))
    ax.plot(range(1, 13), [p["mean_external_inflow"] for p in patterns], marker="o", linewidth=2, label=text("평균 외부 전입", "Mean external inflow"))
    ax.plot(range(1, 13), [p["mean_external_outflow"] for p in patterns], marker="s", linewidth=2, label=text("평균 외부 전출", "Mean external outflow"))
    ax.set_xticks(range(1, 13))
    ax.set_xlabel(text("월", "Calendar month"))
    ax.set_ylabel(text("월평균 이동자수 (명)", "Mean monthly movers"))
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=10)
    finish(fig, "03_monthly_pattern.png", text("반복 패턴을 탐색하는 단순 월별 평균. 추세 조정·계절성 분해 결과가 아니며 원인을 입증하지 않음.", "Descriptive averages, not detrended seasonal decomposition or evidence of causes."))

    metrics_rows = []
    for i, row in enumerate(rows):
        entry = {key: value for key, value in row.items() if key != "date"}
        for metric in METRICS:
            value = moving[metric][i]
            # 이동평균의 첫 11칸은 원자료 결측이 아니라 계산에 필요한 기간 부족이다.
            entry[f"{metric}_ma12"] = "" if math.isnan(value) else value
        metrics_rows.append(entry)
    save_csv(results / "monthly_metrics.csv", metrics_rows)
    save_csv(results / "monthly_pattern.csv", patterns)
    validation.update({
        "analysis_methods": ["trailing_12_month_mean", "calendar_month_means_complete_years_only"],
        "complete_years_for_monthly_pattern": complete_years,
        "ma12_initial_undefined_months": min(WINDOW - 1, len(rows)),
        "python_version": platform.python_version(),
        "matplotlib_version": matplotlib.__version__,
        "korean_labels_available": ko,
        "outlier_assessment": "not_performed; no deletion or imputation",
        "interpretation_status": "not_written; learner review required",
        "source_scope": "uploaded snapshot; no live data fetch",
    })
    (results / "validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[PASS] 48120 Changwon | {period} | {len(rows)} months")
    print("[PASS] Raw data preserved; region, missing months, duplicates and identities checked")
    print("[PASS] 3 charts saved to images/")
    print("[PASS] Metrics and validation saved to results/")
    print("[NEXT] Review charts and evidence before writing REPORT.md")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, csv.Error) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        sys.exit(1)
