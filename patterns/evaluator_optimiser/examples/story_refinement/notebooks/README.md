# story_refinement — Notebook

[evaluator_optimiser-ko.ipynb](evaluator_optimiser-ko.ipynb)에서 Agent 정의, 실행 흐름, 결과 확인, 작은 실습을 단계별로 진행합니다.

## 로컬 실행

1. [uv 환경 설정](../../../../../docs/setup.md)에 따라 커널을 준비합니다.
2. `evaluator_optimiser-ko.ipynb`를 열고 `Agent Pattern Examples` 커널을 선택합니다.
3. 기본값에서는 API 호출을 생략합니다. API 실행을 원하면 설정 셀의 `RUN_API=True`로 변경합니다.
4. Restart & Run All로 위에서 아래로 실행합니다. 기존 환경 변수를 우선 사용하고 `.env.local`이 있으면 읽습니다. 오프라인 실행에는 키나 `.env.local`이 필요하지 않습니다.

## Colab 실행

1. [Colab에서 열기](https://colab.research.google.com/github/ksmin23/agent-pattern-examples/blob/main/patterns/evaluator_optimiser/examples/story_refinement/notebooks/evaluator_optimiser-ko.ipynb)를 클릭합니다. 파일을 다운로드했다면 Colab의 **파일 → 노트북 업로드**로 열 수도 있습니다. 저장소 복제나 Drive 마운트는 필요하지 않습니다.
2. 첫 설정 셀부터 실행합니다. Colab에서만 필요한 패키지를 설치하며 CPU 런타임으로 실행할 수 있습니다. 이미 다른 SDK 버전을 import했다면 런타임을 다시 시작하세요.
3. 오프라인 실습은 기본 `RUN_API=False`로 실행합니다. 실제 API 실행에는 Colab Secrets에 기존 키를 `OPENAI_API_KEY`로 등록하고 Notebook 접근 권한을 허용한 뒤 `RUN_API=True`로 변경합니다.

키는 환경 변수, 선택적 `.env.local`, Colab Secrets 순서로 사용하며 Secrets는 실제 API 실행 시에만 조회합니다. 로컬 키 파일은 Colab에 자동 전달되지 않습니다. 키 값은 출력하거나 파일에 저장하지 않습니다.

모델은 `AGENT_MODEL` 환경 변수 또는 설정 셀에서 변경합니다. 후반 독립 실행 예제는 호출 셀의 `run_api=True`를 별도로 설정해야 합니다. 실제 실행에는 모델 API 비용이 발생할 수 있습니다.

Colab Secrets 처리는 [공식 구현](https://github.com/googlecolab/colabtools/blob/main/google/colab/userdata.py)의 조회 API와 접근 오류를 따릅니다.

[소스 코드](../src/main.py) · [예제 안내](../README.md) · [검증 결과](../../../../../docs/notebook-validation.md)

현재는 `evaluator_optimiser-ko.ipynb` 하나에 단계별 설명, 실습 과제와 독립 실행 예제를 함께 제공합니다. 추가 실습은 해당 Notebook의 **직접 바꿔보기** 섹션에 작성하세요.
