# Triage hand-off: language_routing

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ksmin23/agent-pattern-examples/blob/feat/workflow-planning-colab/patterns/triage_handoff/examples/language_routing/notebooks/triage_handoff-ko.ipynb)

요청의 언어에 따라 전문 에이전트에게 응답의 제어권을 넘깁니다.

## 실행

ZIP을 압축 해제하고 language_routing 폴더로 이동하세요. Python 3.10 이상과 uv가 필요합니다.

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

[한국어 Notebook](notebooks/triage_handoff-ko.ipynb)은 같은 패턴을 셀 단위로 실습하도록 구성했습니다. Notebook은 로컬 Jupyter와 Colab에서 실행하며 `RUN_API=False`가 기본값입니다. `.env.local`은 선택 사항이고, 실제 API 실행 시 환경 변수에 키가 없으면 Colab Secrets의 `OPENAI_API_KEY`를 읽습니다. [환경별 실행 안내](notebooks/README.md)를 참고하세요. CLI는 환경 변수를 직접 준비하고 실행하면 실제 API를 호출합니다.

Notebook은 `AGENT_MODEL`로 모델을 지정합니다(기본값 `gpt-5.6-luna`). CLI의 모델 설정은 `src/`에 정의되어 있으며 이 환경 변수를 사용하지 않습니다.

| 항목 | CLI (`src/main.py`) | Notebook |
|---|---|---|
| 입력·대화 | 터미널 입력을 반복해서 받고 대화 이력을 다음 실행에 전달합니다. | 셀의 `question`으로 단일 요청을 실행합니다. |
| 실행·출력 | `Runner.run_streamed()`로 응답을 스트리밍합니다. | `await Runner.run()`이 완료된 뒤 최종 응답을 표시합니다. |
| 검증 | 응답을 터미널에서 확인합니다. | 기본 프랑스어 요청에 대해 handoff 이벤트와 최종 담당 `French specialist`를 assertion으로 확인합니다. 질문의 언어를 바꾸면 검증 조건도 조정해야 합니다. |

Notebook 후반의 독립 실행 예제는 별도의 `run_api=False` 인수를 사용합니다. 앞부분의 `RUN_API`를 변경해도 이 인수는 바뀌지 않습니다.

## 포함 파일

- src/: 실행 진입점과 모든 Python 보조 모듈 (폴더 구조 유지)
- requirements.txt: PyPI 설치 의존성
- THIRD_PARTY_NOTICES.md: 원본 저작권 및 MIT 고지
- UPSTREAM.json: 포함된 upstream 파일의 출처와 해시

웹 튜토리얼: https://agent-pattern-examples.vercel.app/patterns/triage_handoff/

src/main.py만 따로 실행하지 말고 src/ 전체를 함께 유지한 상태에서 위 명령으로 실행하세요.
