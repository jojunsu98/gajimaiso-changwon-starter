# 가지마이소창원

창원시 인구이동 추세 분석과 정착 지원 시사점. KOSIS 자료의 2016-01~2026-08, 128개월을 분석한 프로젝트입니다.

- [분석 보고서](gajimaiso-changwon/REPORT.md)
- [데이터·분석 방법과 상세 실행 안내](gajimaiso-changwon/README.md)
- [실행·검증 기록](gajimaiso-changwon/RUN_LOG.md)

## Windows에서 실행

Python 3.10 이상이 필요합니다. 실제 검증 환경은 Python 3.12.10 / Matplotlib 3.10.8입니다.
PowerShell에서 이 README가 있는 **저장소 루트**를 연 뒤 실행합니다. 기존 루트 가상환경이 있으면 재사용합니다.

```powershell
python --version
if (-not (Test-Path -LiteralPath '.\.venv\Scripts\python.exe')) { python -m venv .venv }
$python = (Resolve-Path -LiteralPath '.\.venv\Scripts\python.exe').Path
Set-Location -LiteralPath '.\gajimaiso-changwon'
& $python -m pip install -r requirements.txt
& $python analysis.py
```

각 명령이 성공한 뒤 다음 명령을 실행합니다. `python` 대신 `py`를 사용하는 환경은 버전 확인과 가상환경 생성 명령만 `py`로 바꿉니다. 활성화 스크립트나 보안 설정 변경, API 키는 필요하지 않습니다. 인터넷 연결은 패키지 설치 시 필요합니다.

분석은 원자료를 보존하며 하위 프로젝트의 정제 CSV, `images/` PNG 3개, `results/` CSV 2개와 `validation.json`을 갱신합니다. 기존 결과도 저장소에 포함되어 있습니다. `.venv`와 글꼴 캐시는 Git 추적에서 제외합니다.

보고서는 이동 원인이나 서비스 효과를 입증하지 않으며, 2026년 부분 연도는 월별 평균 집계에서 제외합니다.
