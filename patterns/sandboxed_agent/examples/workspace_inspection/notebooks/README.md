# workspace_inspection — Notebook

[sandboxed_agent-ko.ipynb](sandboxed_agent-ko.ipynb)에서 Agent 정의, 실행 흐름, 결과 확인, 작은 실습을 단계별로 진행합니다.

## 실행

1. [uv 환경 설정](../../../../../docs/setup.md)에 따라 커널을 준비합니다.
2. `sandboxed_agent-ko.ipynb`를 열고 `Agent Pattern Examples` 커널을 선택합니다.
3. 기본값에서는 API 호출을 생략합니다. API 실행을 원하면 설정 셀의 `RUN_API=True`로 변경합니다.
4. Restart & Run All로 위에서 아래로 실행합니다. `find_dotenv()`가 현재 위치 또는 상위 디렉터리의 `.env.local`을 찾으며 키 값은 출력하지 않습니다.

모델은 `AGENT_MODEL` 환경 변수 또는 설정 셀에서 변경합니다. Sandbox 예제는 `SANDBOX_MODEL`을 따로 사용합니다. 실행에는 API 비용이 발생할 수 있습니다.

[소스 코드](../src/main.py) · [예제 안내](../README.md) · [검증 결과](../../../../../docs/notebook-validation.md)

추가 실습이 필요하면 `02_exercise.ipynb`, `03_solution.ipynb`를 이 폴더에 추가하세요. 현재는 walkthrough 한 개를 제공합니다.
