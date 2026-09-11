# Sandboxed agent: workspace_inspection

Docker 작업 공간에서 shell 도구로 파일을 읽고, 실행 후 자원을 정리합니다.

## 실행

ZIP을 압축 해제하고 workspace_inspection 폴더로 이동하세요. Python 3.10 이상과 uv가 필요합니다.

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
```

### macOS / Linux

```bash
source .venv/bin/activate
export OPENAI_API_KEY="여기에_본인의_API_키"
python -m src.main --backend docker
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
$env:OPENAI_API_KEY="여기에_본인의_API_키"
python -m src.main --backend docker
```

CLI는 .env.local을 자동으로 읽지 않습니다. API 키를 위와 같이 환경 변수로 설정하세요. 실제 API 호출에는 비용이 발생합니다.

Python 코드는 원본 예제의 실행 흐름과 모델 설정을 보존합니다. Notebook의 RUN_API 스위치와 AGENT_MODEL 설정은 이 CLI에 적용되지 않습니다. 사용 가능한 모델인지 소스 코드에서 확인하세요.

Docker daemon이 실행 중이어야 합니다. 샌드박스 작업에 사용하는 작은 파일은 코드에서 생성합니다. Modal 실행에는 별도 의존성과 계정 설정이 필요하며 여기서는 Docker를 사용합니다.

## Notebook과 CLI의 차이

[한국어 Notebook](notebooks/sandboxed_agent-ko.ipynb)은 같은 패턴을 셀 단위로 실습하도록 구성했습니다. Notebook은 `.env.local`을 탐색해 읽고 `RUN_API=False`를 기본값으로 사용합니다. CLI는 환경 변수를 직접 준비하고 실행하면 실제 API를 호출합니다.

Notebook은 `SANDBOX_MODEL`로 샌드박스 모델을 지정합니다(기본값 `gpt-5.6-sol`). CLI에서는 `--model`을 사용합니다.

| 항목 | CLI (`src/main.py`) | Notebook |
|---|---|---|
| 백엔드·입력 | `--backend`로 Docker 또는 Modal을 선택하고 `--question`, `--model`로 입력을 지정합니다. | Docker 경로만 사용하며 셀의 `question`과 `SANDBOX_MODEL`로 설정합니다. |
| 실행·출력 | `Runner.run_streamed()`로 텍스트와 도구 이벤트를 스트리밍합니다. | `await Runner.run()`이 완료된 뒤 응답을 표시하고 도구 호출 여부를 확인합니다. |
| 코드 구성 | shell 도구 보조 클래스를 `src/workspace_shell.py`에서 가져옵니다. | 같은 역할의 클래스를 코드 셀에 직접 정의합니다. |
| 자원 사용 | CLI 실행 시 샌드박스를 생성합니다. | `RUN_API=False`에서는 Docker 작업과 API 호출을 생략합니다. 실제 실행 후에는 CLI와 마찬가지로 세션을 삭제합니다. |

Notebook 후반의 독립 실행 예제는 별도의 `run_api=False` 인수를 사용합니다. 앞부분의 `RUN_API`를 변경해도 이 인수는 바뀌지 않습니다.

## 포함 파일

- src/: 실행 진입점과 모든 Python 보조 모듈 (폴더 구조 유지)
- requirements.txt: PyPI 설치 의존성
- THIRD_PARTY_NOTICES.md: 원본 저작권 및 MIT 고지
- UPSTREAM.json: 포함된 upstream 파일의 출처와 해시

웹 튜토리얼: https://agent-pattern-examples.vercel.app/patterns/sandboxed_agent/

src/main.py만 따로 실행하지 말고 src/ 전체를 함께 유지한 상태에서 위 명령으로 실행하세요.
