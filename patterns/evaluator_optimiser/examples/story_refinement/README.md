# Evaluator-optimiser: story_refinement

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ksmin23/agent-pattern-examples/blob/feat/workflow-planning-colab/patterns/evaluator_optimiser/examples/story_refinement/notebooks/evaluator_optimiser-ko.ipynb)

이야기 개요를 생성하고, 평가자의 구체적인 피드백을 반영해 다시 작성합니다.

## 실행

ZIP을 압축 해제하고 story_refinement 폴더로 이동하세요. Python 3.10 이상과 uv가 필요합니다.

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

[한국어 Notebook](notebooks/evaluator_optimiser-ko.ipynb)은 같은 패턴을 셀 단위로 실습하도록 구성했습니다. Notebook은 로컬 Jupyter와 Colab에서 실행하며 `RUN_API=False`가 기본값입니다. `.env.local`은 선택 사항이고, 실제 API 실행 시 환경 변수에 키가 없으면 Colab Secrets의 `OPENAI_API_KEY`를 읽습니다. [환경별 실행 안내](notebooks/README.md)를 참고하세요. CLI는 환경 변수를 직접 준비하고 실행하면 실제 API를 호출합니다.

Notebook은 `AGENT_MODEL`로 모델을 지정합니다(기본값 `gpt-5.6-luna`). CLI의 모델 설정은 `src/`에 정의되어 있으며 이 환경 변수를 사용하지 않습니다.

| 항목 | CLI (`src/main.py`) | Notebook |
|---|---|---|
| 입력 | 터미널에서 이야기 주제를 입력합니다. | 셀의 `topic`을 수정합니다. |
| 반복 종료 | `while True`로 평가가 `pass`가 될 때까지 반복하며 코드상 횟수 상한은 없습니다. | `MAX_ROUNDS=3`을 기본값으로 사용하며, 통과하거나 최대 횟수에 도달하면 종료합니다. |
| 평가 기준 | 첫 시도에는 통과시키지 말라는 지침을 사용합니다. | 탐정·우주 배경·구체적인 미스터리·해결 여부를 평가하며 첫 시도에도 통과할 수 있습니다. |
| 평가 입력·형식 | 대화 이력을 평가하고 dataclass로 피드백을 받습니다. | 생성된 개요를 평가하고 Pydantic 모델로 피드백을 받습니다. |

Notebook 후반의 독립 실행 예제는 별도의 `run_api=False` 인수를 사용합니다. 앞부분의 `RUN_API`를 변경해도 이 인수는 바뀌지 않습니다.

## 포함 파일

- src/: 실행 진입점과 모든 Python 보조 모듈 (폴더 구조 유지)
- requirements.txt: PyPI 설치 의존성
- THIRD_PARTY_NOTICES.md: 원본 저작권 및 MIT 고지
- UPSTREAM.json: 포함된 upstream 파일의 출처와 해시

웹 튜토리얼: https://agent-pattern-examples.vercel.app/patterns/evaluator_optimiser/

src/main.py만 따로 실행하지 말고 src/ 전체를 함께 유지한 상태에서 위 명령으로 실행하세요.
