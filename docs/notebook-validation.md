# Notebook 검증 기록

## 최근 오프라인 검증

- 검증 시각: 2026-09-12 09:38:11 KST (JSON 기록: `2026-09-12T00:38:11.564822+00:00`)
- 실행: `python scripts/check_notebooks.py` (`--live` 미사용)
- 환경: `python3 -m venv`로 생성한 임시 가상환경에 `requirements-notebooks.txt` 설치
- Python 3.14.3, openai-agents 0.22.1, openai 3.13.0
- nbclient 0.11.0, nbformat 5.11.1, ipykernel 7.3.0, python-dotenv 1.2.3
- 실행 위치: 각 예제의 `notebooks/` 디렉터리. Notebook마다 별도의 Jupyter 커널 사용
- 결과: Notebook 6개, 코드 셀 39개 모두 통과. 오류 없음, 종료 코드 `0`
- 결과 파일: `.cache/notebook-validation.json` (로컬 생성 파일이며 Git 추적 대상에서 제외)

설정 가이드는 Python 3.12를 권장하지만, 이번 검증에 사용한 Python 버전은 3.14.3입니다. Notebook은 `.env.local`을 읽었으며, 실제 API 호출과 Docker·Modal 작업은 실행하지 않았습니다. API 응답·비용·모델 접근 가능 여부를 이번 결과로 검증한 것은 아닙니다.

| 예제 | 실행 코드 셀 | 오프라인 실행 | 이번 실제 API 실행 |
|---|---|---|---|
| `story_refinement` | 6/6 | 통과 | 수행하지 않음 |
| `translation_candidates` | 6/6 | 통과 | 수행하지 않음 |
| `transient_error_retry` | 6/6 | 통과 | 수행하지 않음 |
| `workspace_inspection` | 8/8 | 통과 | 수행하지 않음 |
| `language_routing` | 6/6 | 통과 | 수행하지 않음 |
| `research_report` | 7/7 | 통과 | 수행하지 않음 |

## 이번 검증 범위

- Notebook 6개의 nbformat 구조 및 코드 셀 39개의 구문 검사. 최상위 `await` 허용.
- 공개 Notebook의 셀 출력·실행 번호가 비어 있고 `RUN_API=False`인지 확인.
- API 키로 의심되는 `sk-` 형태 문자열 검사. 모든 종류의 비밀 정보를 탐지한다는 보장은 없음.
- CLI Python 파일의 기록된 해시 일치 및 실행 전후 소스 변경 여부 확인.
- 각 Notebook의 전체 셀을 순서대로 실행하고 원본 파일 내용이 유지되는지 확인.
- 재시도 예제의 가짜 HTTP 전송 계층에서 429 → 성공 및 정확히 2회 시도 assertion 실행.
- 앞부분 실습은 `RUN_API=False`, 후반 독립 실행 예제는 `run_api=False`로 실행.

검증 스크립트의 커널 통합 테스트 4개도 통과했습니다. API 호출 없는 테스트 Notebook으로 모드 전환, 작업 디렉터리·최상위 await, 원본 보존, 실패 후 다음 Notebook 실행·커널 격리, 오류 원문 제외, 예제 선택, 정적 검사 실패 시 실행 차단을 확인했습니다.

## Colab 대응 검증

2026-09-12에 전체 테스트 16개가 통과했습니다. 위 커널 통합 테스트 4개에 다음 테스트가 포함됩니다.

- `tests/test_workflow_colab.py`의 8개 테스트: Colab 설치 분기와 전체 Notebook의 환경 로딩을 확인합니다. 기존 키 우선 사용, 선택적 환경 파일, 오프라인에서 Secrets를 읽지 않는 동작, 키 누락 및 Secrets 접근 오류 처리를 검사합니다.
- `tests/test_sandbox_colab.py`의 4개 테스트: 백엔드 기본값·선택 오류, Modal 인증, 모의 클라이언트를 통한 Modal 옵션·세션 처리, Docker 오류 경로별 정리 동작을 확인합니다. Modal 1.4.3이 설치된 환경에서 선택적 테스트도 생략 없이 통과했습니다.

별도의 임시 검증 스크립트로 `google.colab`과 Secrets를 모의하고 API·Modal 환경 변수 및 dotenv 로딩을 비활성화한 로컬 Jupyter 커널에서도 Notebook 6개가 모두 통과했습니다. 이 스크립트는 저장소에 포함되어 있지 않으며, 해당 결과와 단위 테스트 결과는 `.cache/notebook-validation.json`에 포함되지 않습니다.

실제 Colab 호스팅 런타임에서의 패키지 설치·Secrets 접근, 실제 Modal 세션 생성, 모델 API 호출은 이번 검증에서 수행하지 않았습니다. 모의 테스트 통과를 실제 원격 실행 확인으로 간주하지 않습니다.

## 과거 실제 API 검증 기록

기존 문서에는 6개 예제 모두 실제 API 실행을 통과한 것으로 기록되어 있습니다. 아래 내용은 과거 기록을 보존한 것이며, 최근 오프라인 검증에서 재확인한 결과가 아닙니다. 기존 문서의 33개 코드 셀 검증도 당시 Notebook 구성에 대한 기록입니다.

당시 기록된 환경은 Python 3.12.13, openai-agents 0.22.1, openai 3.10.0, nbclient 0.11.0, nbformat 5.11.1, ipykernel 7.3.0입니다. Sandbox에는 Docker 29.5.2와 `python:3.14-slim`을 사용했습니다. 기존 기록에는 2026-09-09에 `.env.local` 탐색 방식 변경 후 오프라인 실행을 다시 확인했다는 설명도 있습니다. 실제 API 실행의 정확한 시각과 당시 모델은 현재 오프라인 JSON에 기록되어 있지 않아 이번 결과와 연결하지 않습니다.

과거 실제 API 검증 항목:

- 언어 위임: handoff 이벤트 발생과 최종 French specialist 확인.
- 병렬 실행: 번역 후보 3개 생성 및 선택 결과 확인.
- 재시도: 로컬 가짜 HTTP 전송 계층에서 429 → 성공을 재현하고 정확히 2회 시도했는지 확인. 별도로 실제 모델의 정상 응답 확인.
- 평가·개선: 구조화된 피드백과 통과/최대 횟수 종료 조건 확인. 매 실행에서 개선 반복이 반드시 발생하는 것은 아님.
- 리서치: 계획 생성, 웹 검색 2건, 보고서 생성 확인. 출처의 내용 정확성에 대한 별도 평가를 수행한 것은 아님.
- Sandbox: Docker 작업 공간에서 도구 호출·최종 응답 확인. Notebook의 finally 경로로 세션 삭제.

검증 과정에서 실행 환경의 SOCKS 프록시용 `socksio`를 추가 설치했고, Docker credential helper 경로를 PATH에 추가한 뒤 Sandbox를 재검증했습니다. 환경별 해결 방법은 [설정 가이드](setup.md)에 있습니다.

CLI 원본과 Notebook의 결과 동등성, 비용·속도 벤치마크, 모든 오류 경로에 대한 검증은 수행하지 않았습니다.

## 다시 실행

[환경 설정](setup.md)에 따라 환경을 준비한 뒤 저장소 루트에서:

```bash
python scripts/check_notebooks.py
python scripts/check_notebooks.py --example language_routing
python scripts/check_notebooks.py --live
```

`--live`는 앞부분 실습의 API 호출을 활성화하며 전체 실행 시 선택한 Sandbox 백엔드 작업도 포함합니다. 로컬 기본값은 Docker이며 `SANDBOX_BACKEND=modal`이면 Modal 패키지와 인증이 필요합니다. Colab Notebook의 기본값은 Modal입니다. 후반 독립 실행 예제의 `run_api=False`는 유지합니다. 실제 API와 Modal 사용에는 비용이 발생할 수 있습니다.

결과는 `.cache/notebook-validation.json`에 매번 덮어쓰며, 공개 Notebook은 수정하지 않습니다. 실패하면 종료 코드 `1`을 반환합니다. 이 문서는 자동 갱신되지 않으므로 새 결과를 기록할 때 실행 모드와 환경을 함께 명시하세요.

검증 스크립트의 통합 테스트와 Colab·Sandbox 테스트는 외부 API 호출 없이 실행합니다.

```bash
python -m unittest discover -s tests -v
```

Modal 어댑터 테스트까지 실행하려면 먼저 활성 환경에 `python -m pip install "openai-agents[modal]==0.22.1"`로 선택적 의존성을 설치하세요. Modal 패키지가 없으면 해당 테스트는 건너뜁니다. 이 테스트에는 Modal 인증이 필요하지 않습니다.
