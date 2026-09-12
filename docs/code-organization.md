# 예제 코드 구성과 파일명 기준

## 목적과 적용 범위

예제의 실행 진입점을 쉽게 찾고, 같은 시나리오의 소스와 Notebook을 함께 관리하기 위한 프로젝트 기준입니다. Python이나 OpenAI Agents SDK가 요구하는 파일명 규칙은 아닙니다.

모든 예제는 `patterns/<pattern>/examples/<example>/`에 두고, 소스는 `src/`, Notebook은 `notebooks/`에서 관리합니다. 기존 6개 예제도 이 구조로 재배치했습니다.

## 디렉터리 구조

```text
patterns/
└── evaluator_optimiser/
    ├── README.md
    └── examples/
        └── story_refinement/
            ├── README.md
            ├── src/
            │   └── main.py
            └── notebooks/
                └── evaluator_optimiser-ko.ipynb
```

위 Notebook 파일명은 현재 예제에 있는 파일명입니다. 실제 구현한 파일만 추가합니다.

- 패턴 폴더는 아키텍처를, 예제 폴더는 구체적인 시나리오를 나타냅니다.
- `examples/`는 패턴 바로 아래에서 시나리오들을 모으는 용도로 한 번만 사용합니다.
- 각 시나리오 안에서는 `src/`와 `notebooks/`로 소스와 Notebook을 구분합니다.
- `data/`, `outputs/`, 예제 전용 `requirements.txt`는 필요할 때만 추가합니다.
- 원본 저장소의 `examples/agent_patterns/` 분류를 예제 안에 다시 중첩하지 않습니다.

## 실행 진입점은 main.py

예제의 기본 실행 파일명은 `main.py`로 통일합니다. `story_refinement`처럼 폴더명이 이미 예제의 목적을 설명하므로, 파일명은 실행 진입점임을 나타내면 됩니다.

예를 들어 `llm_as_a_judge.py`를 재구성할 때는 `story_refinement/src/main.py`로 옮깁니다. 원본 파일명과 경로는 출처 기록에 남깁니다.

`main.py`는 입력 수집, 실행 함수 호출, 결과 표시를 담당합니다. import만으로 사용자 입력을 받거나 API를 호출하지 않도록 실행은 `if __name__ == "__main__":` 블록에서 시작합니다.

## 작은 예제는 한 파일로 시작

```text
src/
└── main.py
```

Agent 정의, 간단한 도구, 실행 흐름을 한 파일에서 이해할 수 있다면 그대로 둡니다. 파일을 분리하기 위한 줄 수 기준은 두지 않습니다. 코드 분리로 실행 흐름을 따라가기 어려워진다면 단일 파일을 유지합니다.

## 복잡한 예제는 역할별 분리

Agent나 도구가 늘어나거나, 같은 정의를 여러 실행 경로에서 재사용해야 할 때 분리합니다.

```text
src/
├── __init__.py
├── main.py
├── agents.py
├── tools.py
└── workflow.py
```

| 파일 | 역할 | 분리 시점 |
|---|---|---|
| `main.py` | 입력, 워크플로 호출, 결과 표시 | 항상 기본 진입점으로 사용 |
| `agents.py` | Agent 구성과 생성 함수 | Agent 정의가 실행 흐름을 가리거나 재사용이 필요할 때 |
| `tools.py` | 도구 함수와 도구 구성 | 도구가 여러 개이거나 구현이 길어질 때 |
| `workflow.py` | 계획·위임·병렬 실행·평가 반복 제어 | 제어 흐름을 독립적으로 이해하거나 재사용할 필요가 있을 때 |
| `schemas.py` | 구조화된 입력·출력 타입 | 여러 모듈에서 공유할 타입이 있을 때만 추가 |

표의 파일을 모두 만들 필요는 없습니다. 보조 파일은 `printer.py`, `report_writer.py`처럼 역할을 설명하는 이름을 유지합니다. 패키지 내 모듈명 `agents.py`와 SDK 패키지 `agents`를 구분하도록 로컬 import는 `from .agents import ...`처럼 명시합니다.

## 이름 규칙

- 폴더와 Python 모듈은 `snake_case`를 사용합니다.
- 예제 폴더는 `example_01` 대신 `story_refinement`, `language_routing`처럼 시나리오로 명명합니다.
- 기본 진입점만 `main.py`로 통일하며, 모든 Python 파일을 `main.py`로 바꾸지 않습니다.
- Notebook은 각 예제의 `notebooks/` 안에 `<pattern>-ko.ipynb` 형식으로 두며, 패턴명과 한국어 Notebook임을 나타냅니다. 예: `evaluator_optimiser-ko.ipynb`, `workflow_planning-ko.ipynb`.
- 현재 사용하지 않는 자동 실행용 보조 파일은 미리 추가하지 않습니다.

## 실행 방식과 import

현재 구조에서는 개별 예제 폴더를 작업 디렉터리로 사용합니다. 다음은 저장소 루트에서 실행할 명령 예시입니다.

```bash
cd patterns/evaluator_optimiser/examples/story_refinement
python -m src.main
```

패키지로 모듈을 분리할 때는 `src/__init__.py`를 추가하고 내부 모듈은 상대 import로 참조합니다. 기본 실행 안내는 모듈 실행 방식으로 통일합니다. 다른 예제의 `src`를 직접 import하지 않습니다.

각 예제 README에 실행 명령을 기록합니다. 실행 경로는 파일 이동과 같은 변경에서 갱신합니다.

## Notebook과 소스의 관계

Notebook에는 핵심 Agent 정의와 제어 흐름을 셀 단위로 설명합니다. 학습자가 지침·도구·입력을 직접 바꿀 수 있도록 구성합니다. 공통 도구 등 재사용이 필요한 부분은 같은 예제의 소스에서 가져올 수 있습니다.

Notebook에서 소스를 import한다면 작업 디렉터리와 import 경로를 첫 설정 셀에 명시합니다. 예제마다 `src`라는 이름을 사용하므로 다른 예제로 전환할 때는 새 커널을 사용합니다. Notebook과 CLI는 같은 패턴을 설명하되 입력 방식이나 실습 단계가 다를 수 있으며, 차이는 예제 README에 기록합니다.

## 이름·경로 변경 시 갱신할 항목

1. 실행 진입점과 내부 import를 새 구조에 맞춥니다.
2. 루트·패턴·예제·notebooks README의 코드 링크와 실행 명령을 수정합니다. README와 Notebook의 Colab 링크도 대상 브랜치와 파일 경로에 맞춥니다. 개발 브랜치를 병합하면 기본 브랜치의 링크로 갱신합니다.
3. Notebook의 소스 참조와 데이터 상대 경로를 수정합니다.
4. [UPSTREAM.json](../UPSTREAM.json)의 `local` 경로를 갱신합니다. 원본 저장소, 커밋, 파일 경로는 유지합니다.
5. 내용까지 변경했다면 `modified: true`, `upstream_sha256`, `local_sha256`, `changes`를 기록합니다. 이름·위치만 변경했다면 기존 내용 해시를 유지합니다.
6. 원본 고정 커밋과 [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md)를 보존하고, 예제 README에 재구성한 부분을 설명합니다.
7. Python 구문, 로컬 import, 문서 링크, 실행 위치를 확인합니다. 실제 API 실행 여부는 구분해서 기록합니다.

추가 절차는 [기여 가이드](contributing.md), 환경 준비는 [환경 설정](setup.md)을 참고하세요.
