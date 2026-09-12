# Retry or fallback: transient_error_retry

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ksmin23/agent-pattern-examples/blob/feat/workflow-planning-colab/patterns/retry_or_fallback/examples/transient_error_retry/notebooks/retry_or_fallback-ko.ipynb)

재시도 정책과 백오프를 구성하고, 가짜 HTTP 응답으로 오류 경로를 확인합니다.

## 실행

ZIP을 압축 해제하고 transient_error_retry 폴더로 이동하세요. Python 3.10 이상과 uv가 필요합니다.

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

[한국어 Notebook](notebooks/retry_or_fallback-ko.ipynb)은 같은 패턴을 셀 단위로 실습하도록 구성했습니다. Notebook은 로컬 Jupyter와 Colab에서 실행하며 `RUN_API=False`가 기본값입니다. `.env.local`은 선택 사항이고, 실제 API 실행 시 환경 변수에 키가 없으면 Colab Secrets의 `OPENAI_API_KEY`를 읽습니다. [환경별 실행 안내](notebooks/README.md)를 참고하세요. CLI는 환경 변수를 직접 준비하고 실행하면 실제 API를 호출합니다.

Notebook은 `AGENT_MODEL`로 모델을 지정합니다(기본값 `gpt-5.6-luna`). CLI의 모델 설정은 `src/`에 정의되어 있으며 이 환경 변수를 사용하지 않습니다.

| 항목 | CLI (`src/main.py`) | Notebook |
|---|---|---|
| 오류 재현 | 실제 모델을 호출하며 일시적 오류가 발생할 때 재시도 로그를 출력합니다. | 가짜 HTTP 전송 계층으로 429 → 성공을 재현하고 요청이 정확히 2회였는지 확인합니다. 이 검사는 `RUN_API=False`에서도 실행합니다. |
| 재시도 설정 | 최대 재시도 4회, 초기 지연 0.5초·최대 지연 5초, jitter 사용입니다. | 최대 재시도 2회, 초기 지연 0.1초·최대 지연 1초, jitter 미사용입니다. |
| 정책 구성 | `retry_after()`와 재시도 판단 로그를 포함하고 Agent와 `RunConfig` 양쪽에 설정합니다. | 정책을 간소화해 Agent에 설정하고, 로컬 재현에서는 OpenAI 클라이언트 자체 재시도를 끕니다. |
| 실제 API 실행 | 실행하면 실제 모델을 호출합니다. | 로컬 재현과 별도로 `RUN_API=True`일 때 실제 모델을 호출합니다. |

Notebook 후반의 독립 실행 예제는 별도의 `run_api=False` 인수를 사용합니다. 앞부분의 `RUN_API`를 변경해도 이 인수는 바뀌지 않습니다.

## 포함 파일

- src/: 실행 진입점과 모든 Python 보조 모듈 (폴더 구조 유지)
- requirements.txt: PyPI 설치 의존성
- THIRD_PARTY_NOTICES.md: 원본 저작권 및 MIT 고지
- UPSTREAM.json: 포함된 upstream 파일의 출처와 해시

웹 튜토리얼: https://agent-pattern-examples.vercel.app/patterns/retry_or_fallback/

src/main.py만 따로 실행하지 말고 src/ 전체를 함께 유지한 상태에서 위 명령으로 실행하세요.
