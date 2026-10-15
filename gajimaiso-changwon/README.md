# 가지마이소창원

> 창원시 인구이동 추세 분석과 정착 지원 시사점
> 2016년 1월~2026년 8월 · 기초 분석 실행용 자료

## 현재 단계

원본을 다시 검증하고 그래프 3개와 계산 근거를 생성하는 실행용 프로젝트다.
최종 REPORT.md, 인사이트, 원인 해석, 청년·외국인 분석, 대시보드는 아직 작성하지 않았다.
이 프로젝트는 기존 오이소창원 웹서비스와 별도 폴더에서 작업한다.

## 1. Windows / VS Code에서 실행

압축을 먼저 해제한 뒤, **analysis.py가 직접 보이는 폴더**를 VS Code에서 연다.
`Terminal → New Terminal`에서 PowerShell 터미널을 열고, 아래 명령을 한 줄씩 실행한다.
앞 명령이 끝나고 입력할 수 있는 상태가 되면 다음 명령을 입력한다.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe analysis.py
```

첫 명령에서 Python 3.10 이상인지 확인한다.
`python`이 인식되지 않고 `py --version`은 작동한다면, 가상환경 생성 명령만
`py -m venv .venv`로 바꾸고 나머지 두 명령은 그대로 실행한다.
가상환경 활성화 스크립트는 실행할 필요가 없다.

다시 실행할 때는 마지막 줄만 입력하면 된다.

```powershell
.\.venv\Scripts\python.exe analysis.py
```

프로그램은 웹페이지나 별도 그래프 창을 띄우지 않고 PNG 파일을 저장한다.
인터넷 연결은 라이브러리 설치 시 필요하다. 분석 자체에는 API 키가 필요 없으며,
새 자료를 인터넷에서 자동으로 받아오는 기능은 없다.

## 2. 실행 성공 확인

터미널에 다음 메시지가 표시되고 images 폴더에 PNG 3개가 생기면 기초 실행 성공이다.

```text
[PASS] 48120 Changwon | 2016-01 ~ 2026-08 | 128 months
[PASS] Raw data preserved; region, missing months, duplicates and identities checked
[PASS] 3 charts saved to images/
[PASS] Metrics and validation saved to results/
[NEXT] Review charts and evidence before writing REPORT.md
```

한글 글꼴이 설치되어 있지 않으면 그래프는 영문 표기로 생성된다.
글꼴 파일은 이 프로젝트에 포함하지 않는다.
압축파일에는 테스트에서 생성한 PNG와 results 결과를 넣지 않았다.
사용자 환경에서 직접 실행해 생성 여부를 확인한다.

## 3. 파일의 역할

| 파일 | 역할 |
|---|---|
| `analysis.py` | 원본 재검증, 이동평균·월별 평균 계산, 그래프 3개 생성 |
| `prepare_data.py` | 이전에 제공한 정제 코드. analysis.py가 내부에서 호출 |
| `requirements.txt` | 설치할 그래프 라이브러리 버전 |
| `data/raw/migration_raw.csv` | 사용자가 다운로드한 KOSIS 원본의 이름만 변경한 사본 |
| `data/raw/kosis_metadata.txt` | 사용자가 받은 통계표 메타자료 원본 사본 |
| `data/changwon_migration_monthly_clean.csv` | 128개월 정제본. 실행할 때 원본으로부터 재생성 |
| `images/` | 실행 후 그래프 3개를 저장하는 폴더 |
| `results/` | 실행 후 계산 근거 CSV와 검증 JSON을 저장하는 폴더 |

`data/raw` 원본은 수정하지 않는다. 재실행 시 파생 정제본과 동일한 이름의 결과 파일을 갱신한다.

## 4. 그래프와 분석 방법

### 01_external_trend.png — 외부 전입·전출과 12개월 이동평균

분석 질문: 창원으로 들어오고 나가는 규모는 시간에 따라 어떻게 변했는가?
당월과 직전 11개월 평균을 함께 표시해 월별 진동과 더 완만한 흐름을 나란히 살펴본다.
미래 값이나 보간값은 사용하지 않는다. 첫 11개월의 이동평균은 계산할 수 없어 비워 둔다.
이는 원자료에 결측이 있다는 뜻이 아니다. 모든 원자료 월은 그래프에 유지한다.

### 02_net_migration.png — 월별 순이동

분석 질문: 순유입·순유출의 규모는 어느 시점에 커지거나 작아졌는가?
순이동 = 전입 - 전출이며, 0보다 작으면 순유출, 크면 순유입이다.
순이동을 출생·사망 등을 포함한 전체 인구 증감으로 해석하지 않는다.

### 03_monthly_pattern.png — 1~12월의 평균 이동 규모

분석 질문: 같은 달에 반복적으로 높은 이동 규모가 관찰되는가?
2016~2025년의 완결된 10개 연도만 사용해 각 달에 같은 수의 연도가 기여하도록 한다.
부분 연도인 2026년은 이 그래프에서만 제외한다. 앞의 두 그래프에는 2026년 8월까지 포함한다.
이 결과는 추세 조정이나 시계열 분해가 아닌 단순 월별 평균이므로,
반복 패턴 탐색의 출발점이지 계절성이나 원인의 확정적 증거가 아니다.

## 5. 계산값과 검증 기록

- `results/monthly_metrics.csv`: 원래 월별 항목과 12개월 이동평균. 그래프 수치 검증용.
- `results/monthly_pattern.csv`: 각 달 평균 전입·전출·순이동과 기여 연도 수.
- `results/validation.json`: 원본 SHA-256, 선택·제외한 지역, 기간, 중복·결측·합계식 검증,
  Python/Matplotlib 버전, 이동평균의 첫 11개 미정의값, 완결 연도 목록.

기초 정제는 지역코드 `48120`을 정확히 선택하고, 월 연속성·월/항목 중복·비수치값·음수 인원·
총계와 세부 항목의 합계·순이동식을 검사한다.

정제본의 주요 항목:

| 열 | 의미 |
|---|---|
| `month` | 시점(YYYY-MM) |
| `total_inflow`, `total_outflow` | 창원시 내부 이동을 포함한 원본 총전입·총전출 |
| `within_city_movement` | 창원시 내부 이동 |
| `external_inflow` | 총전입 - 내부 이동 = 시도내 시군구간 전입 + 시도간 전입 |
| `external_outflow` | 총전출 - 내부 이동 = 시도내 시군구간 전출 + 시도간 전출 |
| `net_migration` | 전입 - 전출. 내부 이동을 양쪽에서 빼도 차이는 동일 |

숫자가 크거나 작다는 이유만으로 관측치를 삭제하지 않는다.
이상치 탐지·발생 배경 검토는 아직 별도 수행하지 않았으며, 보간·대체·삭제는 적용하지 않았다.

## 6. 데이터 출처와 범위

- 원본 파일명: `시군구별_이동자수_20261015174157.csv`
- 메타자료 파일명: `101_DT_1B26001_A01_20261015174223.txt`
- 통계표: KOSIS 「시군구별 이동자수」 / 국내인구이동통계
- 표 ID: `DT_1B26001_A01`
- 메타자료 표시 출처와 시각: 국가데이터처, 2026.10.15 17:42
- URL: https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1B26001_A01
- 단위: 명 / 분석 대상: `48120 창원시` / 기간: 2016.01~2026.08
- 주석에 따르면 2010.07.01 통합 창원시가 신설되었으며, 창원의 일반구는 이 표에서 별도 집계하지 않는다.
- 원본의 경상남도 전체 및 통합 전 지역코드 행은 분석에서 제외한다.
- 이 자료에는 연령, 외국인 구분, 개인별 재전출 이력, 이동 사유가 없다.
  청년·외국인의 특성, 재전출률, 이동 원인, 서비스 효과를 이 파일만으로 판단하지 않는다.
- 여러 달을 합친 이동자수를 기간 전체의 중복 없는 고유 인원으로 간주하지 않는다.
- 2026년 누계를 이후 비교할 때는 전년의 같은 월 범위와 비교한다.

출처와 내려받은 시점을 유지한다. 공개 저장소에 재배포하기 전 KOSIS와 원자료 제공기관의
이용·재배포 조건을 확인한다. 이 묶음은 원자료에 새 라이선스를 부여하지 않는다.
비공개 코디세이 과제 원문이나 기존 팀의 비공개 문서는 포함하지 않았다.

## 7. 재현성·실행 기록

직접 의존성은 `matplotlib==3.10.8`이며, 데이터 정제·집계는 Python 표준 라이브러리를 사용한다.
분석 보조 환경에서 실제 실행하고, 3개 PNG와 계산 근거가 생성되는지 확인했다.
검증에 사용한 Python/Matplotlib 버전은 해당 실행의 `results/validation.json`에 남는다.
이는 사용자의 Windows 환경에서 실행됐다는 의미는 아니다.

공식 실행 안내 참고:
- Python venv: https://docs.python.org/3/library/venv.html
- requirements 설치: https://docs.python.org/3/tutorial/venv.html
- Matplotlib 3.10.8 의존성: https://matplotlib.org/3.10.8/install/dependencies.html
- VS Code 터미널: https://code.visualstudio.com/docs/terminal/basics

## 8. 다음 작업

실행 결과를 확인한 뒤, 각 질문에 답할 관찰 수치를 고르고 근거와 가설을 구분해 해석한다.
이상치 후보와 자료 한계도 검토한다. 그 이후 REPORT.md에 질문, 데이터 설명, 정제 기준,
그래프, 근거가 있는 인사이트 3개 이상, 결론·한계, AI 사용 로그를 작성한다.

AI 보조 범위는 데이터 구조 확인, 정제·그래프 코드 작성과 실행 검증이다.
최종 보고서의 AI 사용 로그에는 실제 사용 작업·이유·검증 방법을 작성하고,
사용자가 아직 하지 않은 실행·검토를 완료했다고 쓰지 않는다.
