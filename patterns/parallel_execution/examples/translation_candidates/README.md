# Parallel execution: translation_candidates

번역 후보 세 개를 병렬로 생성한 뒤 선택 에이전트가 최종 결과를 고릅니다.

## 실행

ZIP을 압축 해제하고 translation_candidates 폴더로 이동하세요. Python 3.10 이상과 uv가 필요합니다.

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
```

### macOS / Linux

```bash
source .venv/bin/activate
export OPENAI_API_KEY="여기에_본인의_API_키"
python -m src.main
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
$env:OPENAI_API_KEY="여기에_본인의_API_키"
python -m src.main
```

CLI는 .env.local을 자동으로 읽지 않습니다. API 키를 위와 같이 환경 변수로 설정하세요. 실제 API 호출에는 비용이 발생합니다.

Python 코드는 원본 예제의 실행 흐름과 모델 설정을 보존합니다. Notebook의 RUN_API 스위치와 AGENT_MODEL 설정은 이 CLI에 적용되지 않습니다. 사용 가능한 모델인지 소스 코드에서 확인하세요.

## Notebook과 CLI의 차이

[한국어 Notebook](notebooks/parallel_execution-ko.ipynb)은 같은 패턴을 셀 단위로 실습하도록 구성했습니다. Notebook은 `.env.local`을 탐색해 읽고 `RUN_API=False`를 기본값으로 사용합니다. CLI는 환경 변수를 직접 준비하고 실행하면 실제 API를 호출합니다.

Notebook은 `AGENT_MODEL`로 모델을 지정합니다(기본값 `gpt-5.6-luna`). CLI의 모델 설정은 `src/`에 정의되어 있으며 이 환경 변수를 사용하지 않습니다.

| 항목 | CLI (`src/main.py`) | Notebook |
|---|---|---|
| 입력 | 터미널에서 번역할 문장을 입력합니다. | 셀의 `message`를 수정합니다. |
| 후보 수 | 번역 실행 3개가 코드에 고정되어 있습니다. | `CANDIDATES=3`이 기본값이며 셀에서 1~5개로 조정합니다. |
| 결과 확인 | 후보와 최종 선택 결과를 터미널에 출력합니다. | 후보·선택 결과·소요 시간을 출력하고 후보 수와 비어 있지 않은 응답을 assertion으로 확인합니다. |

Notebook 후반의 독립 실행 예제는 별도의 `run_api=False` 인수를 사용합니다. 앞부분의 `RUN_API`를 변경해도 이 인수는 바뀌지 않습니다.

## 포함 파일

- src/: 실행 진입점과 모든 Python 보조 모듈 (폴더 구조 유지)
- requirements.txt: PyPI 설치 의존성
- THIRD_PARTY_NOTICES.md: 원본 저작권 및 MIT 고지
- UPSTREAM.json: 포함된 upstream 파일의 출처와 해시

웹 튜토리얼: https://agent-pattern-examples.vercel.app/patterns/parallel_execution/

src/main.py만 따로 실행하지 말고 src/ 전체를 함께 유지한 상태에서 위 명령으로 실행하세요.
