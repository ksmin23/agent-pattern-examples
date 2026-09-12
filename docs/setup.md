# 환경 설정

## uv 가상환경

Python 3.12와 uv를 사용합니다. 저장소 루트에서:

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r requirements-notebooks.txt
source .venv/bin/activate
python -m ipykernel install --prefix "$VIRTUAL_ENV" --name agent-pattern-examples --display-name "Agent Pattern Examples"
python -m jupyterlab
```

Windows에서는 `uv pip install --python .venv/Scripts/python.exe ...`와 `.venv\Scripts\Activate.ps1`을 사용합니다. 위 설치 명령은 Jupyter 및 검증 도구와 공통 SDK 의존성을 함께 설치합니다. CLI 소스만 실행할 때는 `requirements.txt`만 설치해도 됩니다. Agents SDK는 PyPI의 `openai-agents[docker]==0.22.1`에서 설치되므로 GitHub checkout이나 Git 기반 패키지 설치가 필요하지 않습니다.

로컬 Notebook은 `find_dotenv(".env.local", usecwd=True)`로 현재 작업 디렉터리부터 상위 디렉터리의 선택적 `.env.local`을 탐색합니다. 기존 환경 변수가 있으면 그 값이 우선합니다. 오프라인 실행에는 파일이나 API 키가 필요하지 않습니다. 키를 Notebook이나 출력에 저장하지 마세요. CLI 소스는 환경 파일을 자동으로 읽지 않으므로 환경 변수를 미리 설정해야 합니다.

SOCKS 프록시를 사용하는 환경에서 `socksio` 누락 오류가 발생하면 가상환경에 다음을 추가합니다.

```bash
uv pip install --python .venv/bin/python "httpx[socks]"
```

## 소스 예제 실행

예제마다 독립적인 `src/` 패키지가 있으므로 해당 예제 폴더에서 실행합니다. 예를 들어 저장소 루트에서:

```bash
cd patterns/triage_handoff/examples/language_routing
python -m src.main
```

다른 예제는 해당 README의 명령을 사용하세요.

## Notebook 실행과 검증

각 예제의 `notebooks/<pattern>-ko.ipynb`를 열고 `Agent Pattern Examples` 커널을 선택하세요. Notebook 폴더와 저장소 루트 모두에서 초기화할 수 있습니다.

- 기본 `RUN_API=False`: Agent 정의와 오프라인 검증만 수행합니다.
- 설정 셀에서 `RUN_API=True`: 앞부분 실습의 모델 호출 셀을 실행합니다. API·웹 검색 비용이 발생할 수 있습니다.
- 후반 독립 실행 예제는 호출 셀의 `run_api=False`를 별도로 `True`로 변경해야 합니다. 앞부분의 `RUN_API` 설정은 이 인수에 적용되지 않습니다.
- 모델 기본값은 `gpt-5.6-luna`이며 `AGENT_MODEL`로 변경할 수 있습니다. Sandbox는 별도 `SANDBOX_MODEL`을 사용하며 기본값은 `gpt-5.6-sol`입니다.
- Notebook은 `await Runner.run(...)`을 사용합니다. Jupyter의 실행 중인 이벤트 루프 안에서 `asyncio.run()`을 사용하지 않습니다.
- 실행 뒤 커밋 전에는 모든 셀 출력과 실행 번호를 지웁니다.

아래 명령은 디스크의 Notebook을 변경하지 않고 실제 Jupyter 커널에서 셀을 순서대로 검증합니다.

```bash
python scripts/check_notebooks.py
python scripts/check_notebooks.py --live
python scripts/check_notebooks.py --live --example language_routing
```

`--live`는 앞부분 실습의 실제 API 호출을 켜며, 후반 독립 실행 예제의 `run_api=False`는 유지합니다. 전체 실행 시 로컬 기본 설정에서는 Sandbox용 Docker도 필요합니다. 결과는 `.cache/notebook-validation.json`에 저장합니다. 실패 시 종료 코드는 1입니다. [최근 검증 결과](notebook-validation.md)를 참고하세요.

## Colab 실행

6개 Notebook 모두 Colab을 지원합니다. 각 패턴 README의 **Colab에서 열기** 또는 예제 README·Notebook 상단의 **Open in Colab** 배지를 사용하세요. 개발 브랜치 링크는 해당 브랜치를 GitHub에 푸시한 뒤 사용할 수 있습니다.

첫 설정 셀은 Colab에서만 필요한 패키지를 설치합니다. 일반 Notebook은 `openai-agents==0.22.1`, Sandbox는 `openai-agents[modal]==0.22.1`을 사용하며 `python-dotenv`도 설치합니다. 저장소 checkout이나 Drive 연결은 필요하지 않습니다. 기본 오프라인 실행에는 API 키나 `.env.local`이 필요하지 않습니다. 실제 API 실행은 Colab Secrets에 `OPENAI_API_KEY`를 등록하고 Notebook 접근을 허용한 뒤 `RUN_API=True`로 켭니다. 환경 변수에 이미 키가 있으면 우선 사용합니다. 로컬 `.env.local`은 Colab에 자동 전달되지 않습니다.

Sandbox Notebook은 Colab에서 원격 Modal을 사용하므로 `MODAL_TOKEN_ID`, `MODAL_TOKEN_SECRET`도 Secrets에 등록해야 합니다. Modal 계정과 별도 사용료가 필요하며, 오프라인 실행은 토큰 없이 가능합니다. [Sandbox Notebook 안내](../patterns/sandboxed_agent/examples/workspace_inspection/notebooks/README.md)를 참고하세요.

## Sandbox 예제

Notebook의 기본 백엔드는 로컬에서 Docker, Colab에서 Modal입니다. `SANDBOX_BACKEND=docker` 또는 `SANDBOX_BACKEND=modal` 환경 변수로 변경할 수 있습니다. 실제 실행에는 선택한 백엔드의 패키지와 인증·실행 환경이 필요합니다. 이 자동 선택은 Notebook에 적용되며 CLI 실행 방법은 예제 README를 따릅니다.

Docker 백엔드는 실행 중인 Docker daemon이 필요합니다. 공통 의존성에는 SDK의 Docker extra가 포함됩니다.

Docker Desktop의 helper가 설치되어 있지만 PATH에 없다는 오류가 나면 macOS에서는 아래 경로를 추가한 터미널에서 Jupyter를 다시 시작하세요.

```bash
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
```

이 경로는 Docker Desktop을 설치한 macOS 환경에만 해당합니다. Colima 등 다른 환경에서는 자신의 Docker 설정과 credential helper 설치 상태를 확인하세요.

로컬에서도 Modal을 사용하려면 활성화한 가상환경에 추가 패키지를 설치한 뒤 인증을 설정합니다.

```bash
uv pip install --python .venv/bin/python "openai-agents[modal]==0.22.1"
python -m modal setup
export SANDBOX_BACKEND=modal
```

기존 Modal 인증 프로필이나 `MODAL_TOKEN_ID`·`MODAL_TOKEN_SECRET` 환경 변수가 있다면 이를 사용할 수 있습니다. Colab에서는 환경 변수가 없을 때 Secrets에서 두 토큰을 읽습니다. `MODAL_APP_NAME`의 기본값은 `agent-pattern-examples`이며 Sandbox 제한 시간은 300초입니다. 종료 시 세션 삭제를 시도하지만 런타임을 강제로 중단했다면 Modal 대시보드에서 종료 상태를 확인하세요. Modal과 모델 API 사용료는 별도입니다.

## 검증 범위

CLI 소스 해시, Python 구문 및 로컬 import 경로는 정적으로 확인했습니다. Notebook 검증 범위와 결과는 [검증 기록](notebook-validation.md)에 별도로 정리합니다.
