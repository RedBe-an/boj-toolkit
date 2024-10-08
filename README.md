# boj-toolkit
`boj-toolkit`은 Baekjoon Online Judge (BOJ) 문제 해결을 위한 코드 관리, 테스트, 제출 도우미 역할을 하는 커맨드라인 도구입니다. 이 도구는 문제 작업을 간소화하고, 솔루션 테스트와 다양한 프로그래밍 언어 관리를 쉽게 할 수 있도록 도와줍니다.

## 설치
`boj-toolkit`은 pip을 통해 설치할 수 있으며, 설치 후 커맨드 라인에서 도구를 사용할 수 있습니다. 설치하려면 다음 명령어를 실행하세요:

```bash
pip install boj-toolkit
```

이 명령어는 필수 종속성을 설치하고 `boj` 명령어를 시스템에서 전역적으로 사용할 수 있도록 설정합니다.

## 사용법
설치가 완료되면 `boj-toolkit`은 BOJ 문제 해결 프로세스를 돕기 위해 여러 명령어를 제공합니다. 현재 사용할 수 있는 명령어는 `add`와 `test`입니다.

### 문제 추가하기
특정 문제 작업을 시작하려면 문제 ID와 함께 `add` 명령어를 사용하세요. 또한 문제를 해결할 프로그래밍 언어도 지정할 수 있습니다. 예를 들어:

```bash
boj add 1000 -l PyPy3
```

이 명령어는 문제 #1000에 대한 작업 환경을 생성하고 언어를 PyPy3로 설정합니다. 그러면 생성된 파일에서 솔루션 코딩을 시작할 수 있습니다.

### 솔루션 테스트하기
솔루션을 구현한 후에는 `test` 명령어를 사용해 빠르게 테스트할 수 있습니다:

```bash
boj test 1000
```

이 명령어는 문제의 샘플 테스트 케이스를 기반으로 솔루션을 실행해 정확성을 확인할 수 있습니다. 터미널에 테스트 케이스의 결과가 표시되며, 어떤 케이스가 통과했는지 또는 실패했는지를 확인할 수 있습니다.

## 사용 가능한 명령어
현재 `boj-toolkit`은 기본적으로 두 가지 주요 명령어를 지원합니다: `add`와 `test`.

- **`add`**: 특정 문제에 대한 작업 환경을 초기화합니다. 문제 ID를 선택하고 프로그래밍 언어를 지정할 수 있습니다.
- **`test`**: 솔루션을 문제의 샘플 테스트 케이스와 비교하여 정확성을 확인합니다.

이 도구는 여전히 활발히 개발 중이며, 향후 업데이트에서 더 많은 명령어가 추가될 예정입니다.

## 기여하기
`boj-toolkit`은 오픈 소스 프로젝트이며, 기여를 환영합니다! 새로운 기능이나 명령어, 개선 사항에 대한 아이디어가 있다면 풀 리퀘스트를 제출하여 프로젝트에 기여할 수 있습니다.

오픈 소스 프로젝트에 기여하는 것이 익숙하지 않거나 시간이 없다면, 프로젝트의 GitHub 페이지에서 이슈를 생성할 수도 있습니다. 
원하는 명령어나 기능을 설명하면, 향후 업데이트를 통해 반영될 수 있습니다.

# 여담
코딩하는 시간보다 테스트 시간이 훨씬 많이 걸렸어요.