# 예제와 Notebook 추가 가이드

## 폴더 규칙

예제는 `patterns/<pattern>/examples/<example>/`에 추가합니다. 실행 진입점은 `src/main.py`로 통일합니다. 폴더명은 `snake_case`로 시나리오를 설명합니다.

```text
<example>/
├── README.md
├── src/
│   ├── __init__.py
│   └── main.py
├── notebooks/
├── data/          # 필요한 경우에만 추가
└── outputs/       # 생성 결과; Git 제외
```

코드 분리와 파일명 기준은 [코드 구성 기준](code-organization.md)을 따릅니다. 원본 저장소의 분류 경로를 중첩하지 않습니다. 미구현 예제를 빈 폴더로 미리 추가하지 않습니다.

## README

- 패턴 README: 개념, 예제 목록, 학습 목표, Notebook 제공 여부.
- 예제 README: 시나리오, 실행 명령, 입력과 출력, Notebook 목록, 출처 및 구현 범위.
- 새 예제를 추가하면 패턴 README의 목록도 갱신합니다.

## Notebook

필요한 순서대로 `01_walkthrough.ipynb`, `02_exercise.ipynb`, `03_solution.ipynb`를 추가하세요. 번호는 각 예제 안에서만 관리합니다.

내용은 학습 목표 → 환경 확인 → 입력·모델 설정 → 도구 정의 → Agent 정의 → 워크플로 실행 → 결과 해석 → 실습 과제 → 출처 순서를 권장합니다. 설명용 Notebook은 핵심 Agent 코드를 셀 안에서 직접 정의하여 수정하고 실험할 수 있게 작성합니다.

- Notebook은 `notebooks/`를 작업 디렉터리로 가정합니다. 첫 부분에 이를 명시하고 필요한 파일은 예제의 `data/` 등 상대 경로로 참조합니다.
- 같은 예제의 `src.*`를 import해야 한다면 상위 예제 디렉터리를 import 경로에 추가하는 셀을 명시합니다. 예제마다 같은 패키지명이 있으므로 다른 예제를 실행할 때는 새 커널을 사용합니다.
- 의존성 설치는 공통 환경 설정에서 수행합니다. Notebook 실행 중 자동 설치하지 않습니다.
- 모델 호출 셀과 비용 발생 여부를 명확히 표시합니다. 키 값은 입력·출력·메타데이터에 저장하지 않습니다.
- Restart & Run All로 실행 순서를 확인한 뒤, 커밋 전에 셀 출력과 실행 번호를 지웁니다. 실제 실행하지 못했다면 해당 상태를 기록합니다.
- 교육용으로 재구성한 Notebook에는 원본 링크와 변경 내용을 적습니다.

## 의존성과 데이터

공통 의존성은 루트 `requirements.txt`, Notebook 도구는 `requirements-notebooks.txt`에서 관리합니다. 예제 전용 의존성이 필요한 경우 예제에 별도 `requirements.txt`를 두고, README에 공통 환경 설치 후 추가로 설치하는 방법을 적습니다.

다른 예제의 코드를 직접 import하지 마세요. `data/`에는 공유 가능한 작은 입력만 두고, 실행 결과는 Git에서 제외되는 `outputs/`에 저장합니다.

## 원본 출처와 검증

원본을 수정 없이 복사할 때 [UPSTREAM.json](../UPSTREAM.json)에 로컬 경로, 원본 경로, SHA-256을 기록합니다. 폴더만 이동하면 로컬 경로만 갱신하고 원본 경로와 해시는 유지합니다. 원본 커밋을 변경하면 SDK 의존성과 전체 원본 목록의 일관성도 확인하세요.

수정한 원본 파일은 `UPSTREAM.json`에서 `modified: true`로 표시하고, `upstream_sha256`, `local_sha256`, `changes`를 기록합니다. 수정하지 않은 파일은 기존 `sha256`을 유지합니다. 예제 README에도 원본 커밋과 변경 내용을 기록합니다. 원본 [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md)의 저작권 고지를 보존하세요.

변경 후 README의 상대 링크, 실행 명령의 작업 위치, 로컬 import 경로를 확인합니다. Notebook을 추가할 때는 파일 형식과 셀 실행 순서도 확인합니다.
