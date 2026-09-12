# Retry or fallback

오류 판단 → 백오프 → 재시도 흐름을 학습합니다.

## 예제 목록

| 예제 | 학습 내용 | 소스 | Notebook |
|---|---|---|---|
| [일시적 오류 재시도](examples/transient_error_retry/) | 오류 판단 → 백오프 → 재시도 | [공식 예제](examples/transient_error_retry/src/) | [Walkthrough](examples/transient_error_retry/notebooks/retry_or_fallback-ko.ipynb) · [Colab에서 열기](https://colab.research.google.com/github/ksmin23/agent-pattern-examples/blob/feat/workflow-planning-colab/patterns/retry_or_fallback/examples/transient_error_retry/notebooks/retry_or_fallback-ko.ipynb) |

현재 예제는 재시도만 구현합니다. 모델 fallback 예제는 아직 없습니다.

새 시나리오는 이 패턴 아래에 별도 예제 폴더로 추가합니다. 각 예제의 구성은 [기여 가이드](../../docs/contributing.md)를 참고하세요.

[전체 패턴 목록](../../README.md)
