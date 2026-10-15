# 가지마이소창원 로컬 실행 기록

- 작업일: 2026-10-15 (Asia/Seoul)
- 작업 범위: `C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter`
- 실제 프로젝트: `C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon`
- 재사용 Python: `C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\.venv\Scripts\python.exe`
- 원자료와 메타자료를 보존하며, 기존 분석 코드로 실행한다. 전역 패키지 설치, 시스템 Python/보안 설정 변경, REPORT.md 작성, 대시보드, 배포, GitHub 업로드는 작업 범위에 포함하지 않는다.

## 1. 위치 및 환경 확인

실행한 파일 목록 명령 (작업 디렉터리: 지정한 상위 폴더):

```powershell
Get-Location
rg --files --hidden -g '!.venv/**' -g '!**/.venv/**' -g '!.git/**' -g '!**/.git/**' -g '!**/node_modules/**' -g '!**/__pycache__/**'
```

종료 코드 0. `gajimaiso-changwon` 하위 폴더에서 `analysis.py`, `requirements.txt`, `README.md`, `prepare_data.py`, 원자료 CSV와 메타자료를 확인했다. 실행 전 images와 results에는 각각 `.gitkeep`만 있었다. `.venv` 내부 파일 목록은 탐색하지 않았다.

다음 명령으로 실행 구조와 기존 가상환경을 확인했다.

```powershell
$root = 'C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter'
$project = Join-Path $root 'gajimaiso-changwon'
$files = @('README.md','analysis.py','prepare_data.py','requirements.txt')
foreach ($name in $files) { [pscustomobject]@{File=$name;Content=(Get-Content -LiteralPath (Join-Path $project $name) -Raw)} | ConvertTo-Json -Compress }
foreach ($path in @((Join-Path $root 'AGENTS.md'),(Join-Path $project 'AGENTS.md'))) { if (Test-Path -LiteralPath $path) { Get-Content -LiteralPath $path -Raw } }
$venvPython = Join-Path $root '.venv\Scripts\python.exe'
[pscustomobject]@{VenvPython=$venvPython;Exists=(Test-Path -LiteralPath $venvPython)} | ConvertTo-Json -Compress
if (Test-Path -LiteralPath $venvPython) { & $venvPython -c 'import sys; print(sys.version); print(sys.executable); print("prefix="+sys.prefix); print("base_prefix="+sys.base_prefix)'; & $venvPython -m pip --version }
```

확인 결과: Python 3.12.10, pip 25.0.1. `sys.prefix`는 상위 폴더의 `.venv`, `base_prefix`는 기존 Python312이다. 가상환경을 재사용한다. 최초 출력에서 한글 경로가 터미널 인코딩 때문에 깨져 보여 이후 실행은 현재 프로세스에 한해 UTF-8 출력을 지정한다.

기존 파일 찾기 실패 원인: `analysis.py`와 `requirements.txt`는 상위 폴더가 아닌 하위 프로젝트 폴더에 있다. 분석 코드는 `Path(__file__).resolve().parent` 기준으로 경로를 처리한다.

실행 도구 오류: 일반 샌드박스 명령은 프로세스 생성 전에 `helper_unknown_error: setup refresh had errors`로 실패했다. 명령이 실행되지 않은 이 실패에는 프로그램 종료 코드가 없다. 읽기 전용 확인은 정상 승인 절차를 통해 실행했으며, 이후 설치/분석도 같은 승인 절차를 사용한다. 실행 정책과 보안 설정은 변경하지 않는다.

## 2. 설치 및 분석

아래에는 실제 실행 시각, 명령, 종료 코드와 출력이 추가된다.


실행 시작 (UTC): 2026-10-15T09:25:55.3409006Z
작업 디렉터리: C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon
현재 프로세스에서 PYTHONUTF8=1, PYTHONIOENCODING=utf-8, MPLCONFIGDIR=results/.matplotlib-cache를 설정했다. 시스템 설정은 바꾸지 않았다. pip 캐시는 --no-cache-dir로 사용하지 않았다.

실행 전 해시/크기/수정 시각 및 결과 존재 상태: results/run_verification.json에 기록.

### 의존성 설치
```powershell
& 'C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\.venv\Scripts\python.exe' -m pip --disable-pip-version-check install --no-cache-dir -r 'C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt'
```
종료 코드: 0
```text
Collecting matplotlib==3.10.8 (from -r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading matplotlib-3.10.8-cp312-cp312-win_amd64.whl.metadata (52 kB)
Collecting contourpy>=1.0.1 (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading contourpy-1.4.0-cp312-cp312-win_amd64.whl.metadata (3.8 kB)
Collecting cycler>=0.10 (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading cycler-0.12.1-py3-none-any.whl.metadata (3.8 kB)
Collecting fonttools>=4.22.0 (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading fonttools-4.67.0-cp312-cp312-win_amd64.whl.metadata (139 kB)
Collecting kiwisolver>=1.3.1 (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading kiwisolver-1.5.1-cp312-cp312-win_amd64.whl.metadata (5.2 kB)
Collecting numpy>=1.23 (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading numpy-2.5.4-cp312-cp312-win_amd64.whl.metadata (6.6 kB)
Collecting packaging>=20.0 (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pillow>=8 (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading pillow-12.3.0-cp312-cp312-win_amd64.whl.metadata (9.3 kB)
Collecting pyparsing>=3 (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading pyparsing-3.3.3-py3-none-any.whl.metadata (5.9 kB)
Collecting python-dateutil>=2.7 (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting six>=1.5 (from python-dateutil>=2.7->matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3))
  Downloading six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Downloading matplotlib-3.10.8-cp312-cp312-win_amd64.whl (8.1 MB)
   ---------------------------------------- 8.1/8.1 MB 15.3 MB/s eta 0:00:00
Downloading contourpy-1.4.0-cp312-cp312-win_amd64.whl (234 kB)
Downloading cycler-0.12.1-py3-none-any.whl (8.3 kB)
Downloading fonttools-4.67.0-cp312-cp312-win_amd64.whl (2.5 MB)
   ---------------------------------------- 2.5/2.5 MB 23.8 MB/s eta 0:00:00
Downloading kiwisolver-1.5.1-cp312-cp312-win_amd64.whl (70 kB)
Downloading numpy-2.5.4-cp312-cp312-win_amd64.whl (12.6 MB)
   ---------------------------------------- 12.6/12.6 MB 19.7 MB/s eta 0:00:00
Downloading packaging-26.3-py3-none-any.whl (129 kB)
Downloading pillow-12.3.0-cp312-cp312-win_amd64.whl (7.2 MB)
   ---------------------------------------- 7.2/7.2 MB 21.2 MB/s eta 0:00:00
Downloading pyparsing-3.3.3-py3-none-any.whl (126 kB)
Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: six, pyparsing, pillow, packaging, numpy, kiwisolver, fonttools, cycler, python-dateutil, contourpy, matplotlib
Successfully installed contourpy-1.4.0 cycler-0.12.1 fonttools-4.67.0 kiwisolver-1.5.1 matplotlib-3.10.8 numpy-2.5.4 packaging-26.3 pillow-12.3.0 pyparsing-3.3.3 python-dateutil-2.9.0.post0 six-1.17.0
```
### 분석 실행
시작 (UTC): 2026-10-15T09:26:26.1437021Z
```powershell
& 'C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\.venv\Scripts\python.exe' 'C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\analysis.py'
```
종료 코드: 0
종료 (UTC): 2026-10-15T09:26:32.9093523Z
```text
[PASS] 48120 Changwon | 2016-01 ~ 2026-08 | 128 months
[PASS] Raw data preserved; region, missing months, duplicates and identities checked
[PASS] 3 charts saved to images/
[PASS] Metrics and validation saved to results/
[NEXT] Review charts and evidence before writing REPORT.md
```
### 설치된 가상환경 패키지
명령: & 'C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\.venv\Scripts\python.exe' -m pip list --format=json --disable-pip-version-check
```json
[{"name": "contourpy", "version": "1.4.0"}, {"name": "cycler", "version": "0.12.1"}, {"name": "fonttools", "version": "4.67.0"}, {"name": "kiwisolver", "version": "1.5.1"}, {"name": "matplotlib", "version": "3.10.8"}, {"name": "numpy", "version": "2.5.4"}, {"name": "packaging", "version": "26.3"}, {"name": "pillow", "version": "12.3.0"}, {"name": "pip", "version": "25.0.1"}, {"name": "pyparsing", "version": "3.3.3"}, {"name": "python-dateutil", "version": "2.9.0.post0"}, {"name": "six", "version": "1.17.0"}]
```
## 3. 독립 재계산 및 산출물 검증
기존 분석 함수를 호출하지 않고 원자료와 결과물을 대조했다. 실제 실행한 PowerShell/Python 명령:
```powershell
$verificationCode = @'
import csv
import hashlib
import io
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

root = Path.cwd()
state_path = root / "results/run_verification.json"
state = json.loads(state_path.read_text(encoding="utf-8-sig"))
assert root == Path(state["project"]), "Unexpected working directory"
assert Path(sys.executable).resolve() == Path(state["python"]).resolve()
assert sys.prefix != sys.base_prefix, "Must use the virtual environment"
assert state["install_exit_code"] == state["analysis_exit_code"] == 0

preserved = []
for before in state["source_before"]:
    path = root / before["path"]
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    stat = path.stat()
    assert digest.upper() == before["sha256"].upper(), str(path)
    assert stat.st_size == before["bytes"], str(path)
    prior_mtime = datetime.fromisoformat(before["last_write_time_utc"]).timestamp()
    assert abs(stat.st_mtime - prior_mtime) < 0.0001, str(path)
    preserved.append({"path": before["path"], "sha256_unchanged": True,
                      "size_unchanged": True, "mtime_unchanged": True})

raw_bytes = (root / "data/raw/migration_raw.csv").read_bytes()
for encoding in ("utf-8-sig", "cp949"):
    try:
        raw_text = raw_bytes.decode(encoding)
        break
    except UnicodeDecodeError:
        pass
else:
    raise AssertionError("Cannot decode source CSV")
raw = list(csv.reader(io.StringIO(raw_text)))
assert len(raw) >= 3 and all(len(row) == len(raw[0]) for row in raw)
keys = []
for month_label, item_label in zip(raw[0][1:], raw[1][1:]):
    match = re.fullmatch(r"M(\d{4})(\d{2})\s+(\d{4})\.(\d{2})", month_label.strip())
    assert match
    year, month, shown_year, shown_month = match.groups()
    assert (year, month) == (shown_year, shown_month)
    assert 1 <= int(month) <= 12
    keys.append((f"{year}-{month}", item_label.split()[0]))
duplicate_keys = sum(n - 1 for n in Counter(keys).values() if n > 1)
assert duplicate_keys == 0
expected = [f"{year}-{month:02}" for year in range(2016, 2027)
            for month in range(1, 13) if f"{year}-{month:02}" <= "2026-08"]
assert len(expected) == 128
assert sorted(set(month for month, item in keys)) == expected
region_codes = [row[0].split()[0] for row in raw[2:]]
duplicate_regions = sum(n - 1 for n in Counter(region_codes).values() if n > 1)
assert duplicate_regions == 0
region_audit = []
for row in raw[2:]:
    invalid = [value for value in row[1:]
               if re.fullmatch(r"[+-]?\d+", value.strip().replace(",", "")) is None]
    region_audit.append({"region": row[0], "data_cells": len(row) - 1,
                         "missing_or_nonnumeric_cells": len(invalid),
                         "missing_or_nonnumeric_tokens": dict(Counter(invalid)),
                         "used_in_analysis": row[0].split()[0] == "48120"})
selected = [row for row in raw[2:] if row[0].split()[0] == "48120"]
assert len(selected) == 1 and selected[0][0].split(maxsplit=1)[1] == "창원시"
assert next(x for x in region_audit if x["used_in_analysis"])["missing_or_nonnumeric_cells"] == 0
source = {}
for (month, item), value in zip(keys, selected[0][1:]):
    source.setdefault(month, {})[item] = int(value.strip().replace(",", ""))

fields = {"T10": "total_inflow", "T20": "total_outflow", "T25": "net_migration",
          "T30": "within_city_movement", "T31": "within_province_inflow",
          "T32": "within_province_outflow", "T40": "interprovince_inflow",
          "T50": "interprovince_outflow"}
for month in expected:
    values = source[month]
    assert set(values) == set(fields)
    assert all(value >= 0 for key, value in values.items() if key != "T25")
    assert values["T10"] - values["T20"] == values["T25"]
    assert values["T10"] == values["T30"] + values["T31"] + values["T40"]
    assert values["T20"] == values["T30"] + values["T32"] + values["T50"]

def read_csv(relative):
    with (root / relative).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

clean = read_csv("data/changwon_migration_monthly_clean.csv")
metrics = read_csv("results/monthly_metrics.csv")
patterns = read_csv("results/monthly_pattern.csv")
assert [row["month"] for row in clean] == expected
assert [row["month"] for row in metrics] == expected
assert len(clean) == len(metrics) == 128
assert [int(row["calendar_month"]) for row in patterns] == list(range(1, 13))
assert len(patterns) == 12
for clean_row, metric_row in zip(clean, metrics):
    assert all(value not in ("", None) for value in clean_row.values())
    assert all(metric_row[key] == value for key, value in clean_row.items())
    assert clean_row["region_code"] == "48120" and clean_row["region_name"] == "창원시"
    values = source[clean_row["month"]]
    for code, name in fields.items():
        assert int(clean_row[name]) == values[code]
    external_in = int(clean_row["external_inflow"])
    external_out = int(clean_row["external_outflow"])
    assert external_in == values["T10"] - values["T30"] == values["T31"] + values["T40"]
    assert external_out == values["T20"] - values["T30"] == values["T32"] + values["T50"]
    assert external_in - external_out == values["T25"]

ma_counts = {}
for metric in ("external_inflow", "external_outflow", "net_migration"):
    name = metric + "_ma12"
    empty_indices = [index for index, row in enumerate(metrics) if row[name] == ""]
    assert empty_indices == list(range(11)), name
    ma_counts[name] = len(empty_indices)
    for index in range(11, 128):
        recomputed = sum(int(row[metric]) for row in metrics[index - 11:index + 1]) / 12
        assert math.isclose(float(metrics[index][name]), recomputed, rel_tol=1e-12)
for pattern in patterns:
    calendar_month = int(pattern["calendar_month"])
    group = [row for row in metrics if int(row["month"][:4]) in range(2016, 2026)
             and int(row["month"][5:]) == calendar_month]
    assert len(group) == int(pattern["n_years"]) == 10
    for metric in ("external_inflow", "external_outflow", "net_migration"):
        recomputed = sum(int(row[metric]) for row in group) / len(group)
        assert math.isclose(float(pattern["mean_" + metric]), recomputed, rel_tol=1e-12)

validation = json.loads((root / "results/validation.json").read_text(encoding="utf-8"))
assert validation["selected_region"].split()[0] == "48120"
assert validation["excluded_region_rows"] == [row[0] for row in raw[2:] if row is not selected[0]]
assert (validation["first_month"], validation["last_month"], validation["months"]) == ("2016-01", "2026-08", 128)
assert validation["source_sha256"] == hashlib.sha256(raw_bytes).hexdigest()
assert validation["raw_numeric_cells"] == 1024
for key in ("missing_months", "duplicate_month_item_pairs", "missing_or_nonnumeric_values"):
    assert validation[key] == 0
assert validation["checks_passed_per_month"] == 4 and validation["months_passing_checks"] == 128
assert validation["complete_years_for_monthly_pattern"] == list(range(2016, 2026))
assert validation["ma12_initial_undefined_months"] == 11
assert validation["imputation_applied"] is False and validation["outlier_deletion_applied"] is False
assert validation["korean_labels_available"] is True

started = datetime.fromisoformat(state["analysis_started_utc"]).timestamp()
finished = datetime.fromisoformat(state["analysis_finished_utc"]).timestamp()
artifacts = []
for before in state["output_before"]:
    path = root / before["path"]
    stat = path.stat()
    assert stat.st_size > 0
    assert started <= stat.st_mtime <= finished + 1, str(path)
    item = {"path": str(path), "bytes": stat.st_size,
            "last_write_time_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            "created_or_updated_in_this_run": True, "readable": True,
            "existed_before_run": before["existed"],
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    if path.suffix == ".png":
        with Image.open(path) as picture:
            assert picture.format == "PNG"
            picture.verify()
        with Image.open(path) as picture:
            picture.load()
            assert picture.size == (1920, 1008)
            item["dimensions"] = list(picture.size)
            assert any(low != high for low, high in picture.convert("RGB").getextrema())
    elif path.suffix == ".csv":
        item["data_rows"] = len(read_csv(before["path"]))
    else:
        json.loads(path.read_text(encoding="utf-8"))
    artifacts.append(item)

state["independent_verification"] = {
    "status": "PASS", "verified_at_utc": datetime.now(timezone.utc).isoformat(),
    "python_executable": sys.executable, "virtual_environment_confirmed": True,
    "preserved_sources_and_code": preserved, "source_encoding": encoding,
    "raw_region_audit": region_audit, "duplicate_region_codes": duplicate_regions,
    "duplicate_month_item_pairs": duplicate_keys, "selected_numeric_cells": 1024,
    "region_code": "48120", "region_name": "창원시",
    "period": {"first": expected[0], "last": expected[-1], "months": len(expected),
               "exact_expected_months_match": True},
    "all_128_monthly_identities_passed": True,
    "internal_moves_excluded_in_both_external_series": True,
    "raw_clean_metrics_values_match": True,
    "ma12_initial_blank_counts": ma_counts,
    "all_remaining_ma12_values_recomputed": True,
    "monthly_pattern_complete_years": list(range(2016, 2026)),
    "monthly_pattern_rows": 12, "years_per_calendar_month": 10,
    "all_monthly_pattern_values_recomputed": True,
    "all_six_required_artifacts_verified": True, "artifacts": artifacts,
    "visual_review": {
        "status": "PASS", "method": "All three original PNG files opened using view_image and visually inspected",
        "korean_text": "readable; no missing glyphs observed",
        "axes": "titles, dates or months, units, ticks and negative values readable",
        "legends": "01 four series and 03 two series readable; 02 single series identified by title and axis, no separate legend",
        "clipping": "no clipped titles, axes, legends or notes observed"
    },
    "scope_limits": [
        "Uploaded local snapshot only; live KOSIS correspondence not independently verified",
        "Outlier and causal assessment not performed; no youth, foreigner or service-effect conclusions",
        "No report, dashboard, deployment or GitHub upload performed"
    ]
}
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(state["independent_verification"], ensure_ascii=False, indent=2))

'@
$verificationCode | & 'C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\.venv\Scripts\python.exe' -
```
검증 종료 코드: 0
```json
{
  "status": "PASS",
  "verified_at_utc": "2026-10-15T09:28:31.979943+00:00",
  "python_executable": "C:\\Users\\user\\OneDrive\\바탕 화면\\gajimaiso-changwon-starter\\.venv\\Scripts\\python.exe",
  "virtual_environment_confirmed": true,
  "preserved_sources_and_code": [
    {
      "path": "data\\raw\\migration_raw.csv",
      "sha256_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    },
    {
      "path": "data\\raw\\kosis_metadata.txt",
      "sha256_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    },
    {
      "path": "analysis.py",
      "sha256_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    },
    {
      "path": "prepare_data.py",
      "sha256_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    },
    {
      "path": "requirements.txt",
      "sha256_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    },
    {
      "path": "README.md",
      "sha256_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    }
  ],
  "source_encoding": "utf-8-sig",
  "raw_region_audit": [
    {
      "region": "48 경상남도",
      "data_cells": 1024,
      "missing_or_nonnumeric_cells": 0,
      "missing_or_nonnumeric_tokens": {},
      "used_in_analysis": false
    },
    {
      "region": "48110 창원시",
      "data_cells": 1024,
      "missing_or_nonnumeric_cells": 0,
      "missing_or_nonnumeric_tokens": {},
      "used_in_analysis": false
    },
    {
      "region": "48120 창원시",
      "data_cells": 1024,
      "missing_or_nonnumeric_cells": 0,
      "missing_or_nonnumeric_tokens": {},
      "used_in_analysis": true
    },
    {
      "region": "48160 마산시",
      "data_cells": 1024,
      "missing_or_nonnumeric_cells": 0,
      "missing_or_nonnumeric_tokens": {},
      "used_in_analysis": false
    },
    {
      "region": "48190 진해시",
      "data_cells": 1024,
      "missing_or_nonnumeric_cells": 0,
      "missing_or_nonnumeric_tokens": {},
      "used_in_analysis": false
    }
  ],
  "duplicate_region_codes": 0,
  "duplicate_month_item_pairs": 0,
  "selected_numeric_cells": 1024,
  "region_code": "48120",
  "region_name": "창원시",
  "period": {
    "first": "2016-01",
    "last": "2026-08",
    "months": 128,
    "exact_expected_months_match": true
  },
  "all_128_monthly_identities_passed": true,
  "internal_moves_excluded_in_both_external_series": true,
  "raw_clean_metrics_values_match": true,
  "ma12_initial_blank_counts": {
    "external_inflow_ma12": 11,
    "external_outflow_ma12": 11,
    "net_migration_ma12": 11
  },
  "all_remaining_ma12_values_recomputed": true,
  "monthly_pattern_complete_years": [
    2016,
    2017,
    2018,
    2019,
    2020,
    2021,
    2022,
    2023,
    2024,
    2025
  ],
  "monthly_pattern_rows": 12,
  "years_per_calendar_month": 10,
  "all_monthly_pattern_values_recomputed": true,
  "all_six_required_artifacts_verified": true,
  "artifacts": [
    {
      "path": "C:\\Users\\user\\OneDrive\\바탕 화면\\gajimaiso-changwon-starter\\gajimaiso-changwon\\images\\01_external_trend.png",
      "bytes": 205856,
      "last_write_time_utc": "2026-10-15T09:26:32.536985+00:00",
      "created_or_updated_in_this_run": true,
      "readable": true,
      "existed_before_run": false,
      "sha256": "bb95ec7c326b628498556fb32285b4fb5efdc35c6ba6c99f30abe5a4c836a313",
      "dimensions": [
        1920,
        1008
      ]
    },
    {
      "path": "C:\\Users\\user\\OneDrive\\바탕 화면\\gajimaiso-changwon-starter\\gajimaiso-changwon\\images\\02_net_migration.png",
      "bytes": 58938,
      "last_write_time_utc": "2026-10-15T09:26:32.706244+00:00",
      "created_or_updated_in_this_run": true,
      "readable": true,
      "existed_before_run": false,
      "sha256": "b47bb764655882a973b4f3ff6b16c451fbe34909320a8b1d1adf5ec1dac17d18",
      "dimensions": [
        1920,
        1008
      ]
    },
    {
      "path": "C:\\Users\\user\\OneDrive\\바탕 화면\\gajimaiso-changwon-starter\\gajimaiso-changwon\\images\\03_monthly_pattern.png",
      "bytes": 106010,
      "last_write_time_utc": "2026-10-15T09:26:32.825280+00:00",
      "created_or_updated_in_this_run": true,
      "readable": true,
      "existed_before_run": false,
      "sha256": "3c5705c8f62932730c0460a8883beb26ead63e5cf7895ad3d132562a271e3558",
      "dimensions": [
        1920,
        1008
      ]
    },
    {
      "path": "C:\\Users\\user\\OneDrive\\바탕 화면\\gajimaiso-changwon-starter\\gajimaiso-changwon\\results\\monthly_metrics.csv",
      "bytes": 14976,
      "last_write_time_utc": "2026-10-15T09:26:32.827817+00:00",
      "created_or_updated_in_this_run": true,
      "readable": true,
      "existed_before_run": false,
      "sha256": "4b6e224404a1b6fffe196e308b77a5aa5b13b807d6ae012fe31cf8c33b36bb5f",
      "data_rows": 128
    },
    {
      "path": "C:\\Users\\user\\OneDrive\\바탕 화면\\gajimaiso-changwon-starter\\gajimaiso-changwon\\results\\monthly_pattern.csv",
      "bytes": 412,
      "last_write_time_utc": "2026-10-15T09:26:32.828780+00:00",
      "created_or_updated_in_this_run": true,
      "readable": true,
      "existed_before_run": false,
      "sha256": "2bfe8d572322256a6a49f62ab9334ac594142f55e0143c5f86587f920028b071",
      "data_rows": 12
    },
    {
      "path": "C:\\Users\\user\\OneDrive\\바탕 화면\\gajimaiso-changwon-starter\\gajimaiso-changwon\\results\\validation.json",
      "bytes": 2338,
      "last_write_time_utc": "2026-10-15T09:26:32.829777+00:00",
      "created_or_updated_in_this_run": true,
      "readable": true,
      "existed_before_run": false,
      "sha256": "5a30fb399e5d1fb4b1d07c5d1d3c762c8492a109aff04d5c371eacfd74af40b3"
    }
  ],
  "visual_review": {
    "status": "PASS",
    "method": "All three original PNG files opened using view_image and visually inspected",
    "korean_text": "readable; no missing glyphs observed",
    "axes": "titles, dates or months, units, ticks and negative values readable",
    "legends": "01 four series and 03 two series readable; 02 single series identified by title and axis, no separate legend",
    "clipping": "no clipped titles, axes, legends or notes observed"
  },
  "scope_limits": [
    "Uploaded local snapshot only; live KOSIS correspondence not independently verified",
    "Outlier and causal assessment not performed; no youth, foreigner or service-effect conclusions",
    "No report, dashboard, deployment or GitHub upload performed"
  ]
}
```
## 4. 시각적 검수 및 완료 범위

- 도구 `view_image`로 images/01_external_trend.png, images/02_net_migration.png, images/03_monthly_pattern.png의 원본 크기 이미지를 모두 열어 직접 확인했다.
- 한글 제목/주석, 축 이름/단위/눈금, 음수 표시가 읽히고, 제목이나 하단 주석이 잘리지 않았다.
- 01의 4개 계열 범례와 03의 2개 계열 범례가 정상 표시된다. 02는 단일 막대 계열로 별도 범례가 없으며 제목과 축에 순이동이 명시돼 있다.
- 최초 11개월 MA12 빈칸은 각 지표에 11개씩 존재하고, 원자료 결측으로 집계하지 않았다.
- 월별 패턴은 2016~2025년의 10개 완결 연도만 사용한다. 2026년 1~8월은 추세/순이동 그래프에 포함되며 연간 총계 비교는 수행하지 않았다.
- 기존 analysis.py, prepare_data.py, requirements.txt, README.md는 수정하지 않았다. data/raw의 CSV와 메타자료는 해시, 크기, 수정 시각이 실행 전과 동일하다.
- 파생 정제본, 요청한 PNG 3개와 CSV 2개/validation.json을 생성·갱신했다. 추가 실행 증거는 RUN_LOG.md와 results/run_verification.json에 기록했다. Matplotlib 글꼴 캐시는 프로젝트 내부 results/.matplotlib-cache에만 저장했다.
- 이 실행은 로컬 제공 파일의 내부 일관성과 산출물을 검증했다. 실시간 KOSIS와의 일치 여부, 이상치 발생 배경, 이동 원인, 청년·외국인 구분 및 서비스 효과는 검증/분석하지 않았다.
- REPORT.md, 대시보드, 배포, GitHub 업로드는 수행하지 않았다.

### 이번 재실행 스크립트
```python
import csv,hashlib,io,json,math,os,re,subprocess,sys,time
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
p=Path.cwd()
def log(s):
    with (p/"RUN_LOG.md").open("a",encoding="utf-8") as f:f.write(s+"\n")
def digest(f):return hashlib.sha256(f.read_bytes()).hexdigest()
names=["data/raw/migration_raw.csv","data/raw/kosis_metadata.txt","analysis.py","prepare_data.py","requirements.txt","README.md","REPORT.md"]
before={n:(digest(p/n),(p/n).stat().st_mtime_ns) for n in names if (p/n).exists()}
outputs=["images/01_external_trend.png","images/02_net_migration.png","images/03_monthly_pattern.png","results/monthly_metrics.csv","results/monthly_pattern.csv","results/validation.json"]
old={n:(p/n).stat().st_mtime_ns if (p/n).exists() else 0 for n in outputs}
assert sys.prefix!=sys.base_prefix
log("\n## 실제 재실행 "+datetime.now().astimezone().isoformat())
log("폴더: "+str(p)+"\nPython: "+sys.executable+"\n"+sys.version)
log("사전 확인: rg --files --hidden (모든 .venv/.git/__pycache__ 제외), Get-Content -LiteralPath로 README.md/analysis.py/prepare_data.py/requirements.txt 읽기, 기존 Python --version 및 -m pip --version. 종료 코드 0; Python 3.12.10, pip 25.0.1. 기존 결과가 이미 존재함을 확인. 일반 실행기의 helper_unknown_error 초기화 실패 후 정상 승인 실행. 시스템/보안 설정 변경 없음.")
log("보존 대상 실행 전 SHA256/mtime_ns:\n"+json.dumps(before,ensure_ascii=False,indent=2))
env=os.environ.copy()
env["MPLCONFIGDIR"]=str(p/"results/.matplotlib-cache")
env["PYTHONIOENCODING"]="utf-8"
def run(args):
    log("명령: "+subprocess.list2cmdline(args))
    r=subprocess.run(args,cwd=p,env=env,capture_output=True,text=True,encoding="utf-8")
    log("종료 코드: "+str(r.returncode)+"\n"+r.stdout+r.stderr)
    print(r.stdout+r.stderr)
    assert r.returncode==0
run([sys.executable,"-m","pip","--disable-pip-version-check","install","--no-cache-dir","-r",str(p/"requirements.txt")])
start=time.time()
run([sys.executable,str(p/"analysis.py")])
end=time.time()
def read(n):
    with (p/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
rows=read("results/monthly_metrics.csv")
clean=read("data/changwon_migration_monthly_clean.csv")
patterns=read("results/monthly_pattern.csv")
v=json.loads((p/"results/validation.json").read_text(encoding="utf-8"))
expected=[f"{y}-{m:02}" for y in range(2016,2027) for m in range(1,13) if f"{y}-{m:02}"<="2026-08"]
assert len(rows)==128 and [r["month"] for r in rows]==expected
assert [r["month"] for r in clean]==expected
raw=list(csv.reader(io.StringIO((p/"data/raw/migration_raw.csv").read_text(encoding="utf-8-sig"))))
assert all(len(r)==len(raw[0]) for r in raw)
keys=[]
for a,b in zip(raw[0][1:],raw[1][1:]):
    m=re.fullmatch(r"M(\d{4})(\d{2})\s+(\d{4})\.(\d{2})",a.strip())
    assert m and m.groups()[:2]==m.groups()[2:]
    keys.append((m[1]+"-"+m[2],b.split()[0]))
assert len(keys)==len(set(keys))==1024
assert len({r[0].split()[0] for r in raw[2:]})==len(raw[2:])
audit=[{"region":r[0],"missing_or_nonnumeric":sum(not bool(re.fullmatch(r"[+-]?\d+",x.strip().replace(",",""))) for x in r[1:])} for r in raw[2:]]
assert all(a["missing_or_nonnumeric"]==0 for a in audit)
selected=[r for r in raw[2:] if r[0].split()[0]=="48120"]
assert len(selected)==1
source={}
for (month,item),value in zip(keys,selected[0][1:]):source.setdefault(month,{})[item]=int(value.replace(",",""))
fields={"T10":"total_inflow","T20":"total_outflow","T25":"net_migration","T30":"within_city_movement","T31":"within_province_inflow","T32":"within_province_outflow","T40":"interprovince_inflow","T50":"interprovince_outflow"}
for r,c in zip(rows,clean):
    assert r["region_code"]=="48120" and r["region_name"]=="창원시"
    assert all(r[k]==value and value!="" for k,value in c.items())
    x=source[r["month"]]
    assert set(x)==set(fields)
    assert all(int(r[n])==x[k] for k,n in fields.items())
    assert all(n>=0 for k,n in x.items() if k!="T25")
    assert x["T10"]-x["T20"]==x["T25"]
    assert int(r["external_inflow"])==x["T10"]-x["T30"]==x["T31"]+x["T40"]
    assert int(r["external_outflow"])==x["T20"]-x["T30"]==x["T32"]+x["T50"]
    assert int(r["external_inflow"])-int(r["external_outflow"])==x["T25"]
for metric in ["external_inflow","external_outflow","net_migration"]:
    assert [i for i,r in enumerate(rows) if r[metric+"_ma12"]==""]==list(range(11))
    for i in range(11,128):
        assert math.isclose(float(rows[i][metric+"_ma12"]),sum(int(r[metric]) for r in rows[i-11:i+1])/12,rel_tol=1e-12)
assert len(patterns)==12 and [int(r["calendar_month"]) for r in patterns]==list(range(1,13))
for r in patterns:
    g=[x for x in rows if x["month"][:4]<"2026" and int(x["month"][5:])==int(r["calendar_month"])]
    assert len(g)==int(r["n_years"])==10
    for metric in ["external_inflow","external_outflow","net_migration"]:
        assert math.isclose(float(r["mean_"+metric]),sum(int(x[metric]) for x in g)/10,rel_tol=1e-12)
assert v["selected_region"]=="48120 창원시"
assert (v["first_month"],v["last_month"],v["months"])==("2016-01","2026-08",128)
assert v["source_sha256"]==digest(p/"data/raw/migration_raw.csv")
assert all(v[k]==0 for k in ["missing_months","duplicate_month_item_pairs","missing_or_nonnumeric_values"])
assert v["complete_years_for_monthly_pattern"]==list(range(2016,2026))
assert v["ma12_initial_undefined_months"]==11
assert not v["imputation_applied"] and not v["outlier_deletion_applied"]
artifacts=[]
for n in outputs:
    f=p/n;s=f.stat()
    assert s.st_size>0 and start<=s.st_mtime<=end+1 and s.st_mtime_ns>old[n]
    if f.suffix==".png":
        with Image.open(f) as im:im.verify()
        with Image.open(f) as im:
            im.load()
            assert im.size==(1920,1008)
    elif f.suffix==".csv":read(n)
    else:json.loads(f.read_text(encoding="utf-8"))
    artifacts.append({"path":str(f),"bytes":s.st_size,"mtime_utc":datetime.fromtimestamp(s.st_mtime,timezone.utc).isoformat(),"readable":True,"updated_this_run":True})
for n,b in before.items():assert (digest(p/n),(p/n).stat().st_mtime_ns)==b
summary={"status":"PASS","install_exit":0,"analysis_exit":0,"analysis_started_utc":datetime.fromtimestamp(start,timezone.utc).isoformat(),"analysis_finished_utc":datetime.fromtimestamp(end,timezone.utc).isoformat(),"region":"48120 창원시","period":"2016-01~2026-08","months":128,"raw_audit":audit,"duplicates":0,"identities_and_internal_exclusion":True,"ma12_initial_blanks":11,"ma12_and_pattern_recomputed":True,"pattern_years":"2016~2025","protected_files_unchanged":list(before),"artifacts":artifacts,"visual_review":"pending"}
log("이번 독립 검증 결과:\n"+json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))

```
실행: 아래 명시한 가상환경 python.exe - 로 표준입력 전달. 현재 폴더: 실제 프로젝트.

## 실제 재실행 2026-10-16T00:04:52.952271+09:00
폴더: C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon
Python: C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\.venv\Scripts\python.exe
3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]
사전 확인: rg --files --hidden (모든 .venv/.git/__pycache__ 제외), Get-Content -LiteralPath로 README.md/analysis.py/prepare_data.py/requirements.txt 읽기, 기존 Python --version 및 -m pip --version. 종료 코드 0; Python 3.12.10, pip 25.0.1. 기존 결과가 이미 존재함을 확인. 일반 실행기의 helper_unknown_error 초기화 실패 후 정상 승인 실행. 시스템/보안 설정 변경 없음.
보존 대상 실행 전 SHA256/mtime_ns:
{
  "data/raw/migration_raw.csv": [
    "8fd4d73b3c5fe2adc3de3e308934065ae46788ebde62054b9b3a7986e696a674",
    1792022012000000000
  ],
  "data/raw/kosis_metadata.txt": [
    "d156761d863d85e263c5c3435550c2394763816566f52dd2311ebfeb1920f491",
    1792022012000000000
  ],
  "analysis.py": [
    "804c0d39262ccf61e1cd59f0900465e235ab449899f7161f5612774af729968e",
    1792022176000000000
  ],
  "prepare_data.py": [
    "61b0d1816a63e3ec2a6a2fc6f2803c7230ad503c5eb9d79aa466063b8259bbaf",
    1792022012000000000
  ],
  "requirements.txt": [
    "efb6203fd3df46edfb1da8941d40a91cbaf5a1b1b18d09fee73537a6a6635867",
    1792022012000000000
  ],
  "README.md": [
    "1015490978ca050281652fc36b1342aa45cbfbb5383be59fc6f7210d7a8ee3cf",
    1792022176000000000
  ],
  "REPORT.md": [
    "33b6c41cb9f51ba2fe5295f2b3fbb8a0a55772620285ef7ce2f1ee2de953cb96",
    1792076362354164100
  ]
}
명령: "C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\.venv\Scripts\python.exe" -m pip --disable-pip-version-check install --no-cache-dir -r "C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt"
종료 코드: 0
Requirement already satisfied: matplotlib==3.10.8 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from -r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (3.10.8)
Requirement already satisfied: contourpy>=1.0.1 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (1.4.0)
Requirement already satisfied: cycler>=0.10 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (0.12.1)
Requirement already satisfied: fonttools>=4.22.0 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (4.67.0)
Requirement already satisfied: kiwisolver>=1.3.1 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (1.5.1)
Requirement already satisfied: numpy>=1.23 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (2.5.4)
Requirement already satisfied: packaging>=20.0 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (26.3)
Requirement already satisfied: pillow>=8 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (12.3.0)
Requirement already satisfied: pyparsing>=3 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (3.3.3)
Requirement already satisfied: python-dateutil>=2.7 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (2.9.0.post0)
Requirement already satisfied: six>=1.5 in c:\users\user\onedrive\바탕 화면\gajimaiso-changwon-starter\.venv\lib\site-packages (from python-dateutil>=2.7->matplotlib==3.10.8->-r C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\requirements.txt (line 3)) (1.17.0)

명령: "C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\.venv\Scripts\python.exe" "C:\Users\user\OneDrive\바탕 화면\gajimaiso-changwon-starter\gajimaiso-changwon\analysis.py"
종료 코드: 1
[ERROR] [Errno 22] Invalid argument: 'C:\\Users\\user\\OneDrive\\바탕 화면\\gajimaiso-changwon-starter\\gajimaiso-changwon\\images\\01_external_trend.png'

이번 설치·분석·독립검증 스크립트 종료 코드: 1
