# Workflow planning: research_report

리서치 질문을 검색 계획으로 나누고, 수집한 정보를 하나의 보고서로 종합합니다.

## 실행

ZIP을 압축 해제하고 research_report 폴더로 이동하세요. Python 3.10 이상과 uv가 필요합니다.

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

[한국어 Notebook](notebooks/workflow_planning-ko.ipynb)은 같은 패턴을 셀 단위로 실습하도록 구성했습니다. Notebook은 `.env.local`을 탐색해 읽고 `RUN_API=False`를 기본값으로 사용합니다. CLI는 환경 변수를 직접 준비하고 실행하면 실제 API를 호출합니다.

Notebook은 `AGENT_MODEL`로 모델을 지정합니다(기본값 `gpt-5.6-luna`). CLI의 모델 설정은 `src/`에 정의되어 있으며 이 환경 변수를 사용하지 않습니다.

| 항목 | CLI (`src/main.py`) | Notebook |
|---|---|---|
| 입력·구성 | 터미널에서 질문을 받고 `manager.py`, `agents/`, `printer.py`로 역할을 나눕니다. | 셀의 `query`를 수정하며 Agent 정의와 계획·검색·작성 단계를 셀에서 확인합니다. |
| 검색 규모 | Planner에게 검색어 5~20개를 생성하도록 지시합니다. | 검색어 2개를 생성하도록 지시하며 스키마는 1~2개를 허용합니다. |
| 보고서 | Writer에게 5~10페이지, 최소 1,000단어를 목표로 작성하도록 지시합니다. | 400단어 미만의 짧은 보고서를 작성하도록 지시합니다. |
| 실행·표시 | 보고서 작성에 `Runner.run_streamed()`를 사용하고 Rich로 진행 상황을 표시합니다. | 단계별 `await Runner.run()`과 병렬 검색을 사용하고 결과를 Markdown으로 표시합니다. |

Notebook 후반의 독립 실행 예제는 별도의 `run_api=False` 인수를 사용합니다. 앞부분의 `RUN_API`를 변경해도 이 인수는 바뀌지 않습니다.

## 포함 파일

- src/: 실행 진입점과 모든 Python 보조 모듈 (폴더 구조 유지)
- requirements.txt: PyPI 설치 의존성
- THIRD_PARTY_NOTICES.md: 원본 저작권 및 MIT 고지
- UPSTREAM.json: 포함된 upstream 파일의 출처와 해시

웹 튜토리얼: https://agent-pattern-examples.vercel.app/patterns/workflow_planning/

src/main.py만 따로 실행하지 말고 src/ 전체를 함께 유지한 상태에서 위 명령으로 실행하세요.
