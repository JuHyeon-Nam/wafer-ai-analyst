# GitHub Repository Setup Guide

## 추천 repository 이름

가장 추천:

```text
wafer-ai-analyst
```

이 이름이 좋은 이유:

- 짧고 기억하기 쉽다.
- wafer, AI, analyst라는 핵심 키워드가 들어간다.
- 반도체 데이터 분석 프로젝트라는 느낌이 바로 난다.
- 하이닉스/삼성전자 지원용 포트폴리오에서 설명하기 좋다.

대안:

```text
wafer-electrical-test-ai-agent
semiconductor-wafer-ai-analyst
shot-level-wafer-qc-agent
semiconductor-test-data-ai-agent
```

너무 긴 이름은 GitHub에서 보기 불편하므로 `wafer-ai-analyst`를 1순위로 추천합니다.

## Repository description

GitHub repo 설명 칸에는 아래 문장을 넣으면 됩니다.

```text
AI-assisted analysis tool for semiconductor wafer electrical test data, shot-level anomaly detection, and process issue reasoning.
```

한국어로 의미:

```text
반도체 웨이퍼 전기 측정 데이터를 분석하고, shot 단위 이상 탐지와 공정 이슈 후보 추론을 수행하는 AI 분석 도구
```

## Topics

GitHub repo 생성 후 Topics에 아래 키워드를 추가하면 좋습니다.

```text
semiconductor
wafer
electrical-test
ai-agent
anomaly-detection
streamlit
data-analysis
quality-control
```

## Repository 생성 옵션

GitHub에서 새 repository 만들 때 추천 설정:

```text
Repository name: wafer-ai-analyst
Description: AI-assisted analysis tool for semiconductor wafer electrical test data, shot-level anomaly detection, and process issue reasoning.
Visibility: Public
Add README: 체크하지 않기
Add .gitignore: 체크하지 않기
Choose a license: 체크하지 않기
```

이미 로컬 프로젝트에 README와 .gitignore가 있으므로 GitHub에서 자동 생성하지 않는 것이 좋습니다.

## 친구들 collaborator 추가 방법

GitHub 웹사이트에서:

```text
Repository 접속
-> Settings
-> Collaborators and teams
-> Add people
-> 친구 GitHub ID 입력
-> 권한 선택
-> Add
```

권한은 처음에는 `Write`로 충분합니다.

권한 의미:

- Read: 보기만 가능
- Triage: issue 관리 가능
- Write: 코드 push 가능
- Maintain: repo 설정 일부 관리 가능
- Admin: 거의 모든 설정 변경 가능

팀 프로젝트에서는 친구들에게 `Write` 권한을 주면 됩니다.

## GitHub repo를 만든 뒤 로컬에서 연결하는 명령어

GitHub에서 repo를 만든 뒤, 아래 명령어를 실행하면 됩니다.

```bash
git remote add origin https://github.com/<본인아이디>/wafer-ai-analyst.git
git push -u origin main
```

예시:

```bash
git remote add origin https://github.com/JuHyeon-Nam/wafer-ai-analyst.git
git push -u origin main
```

이미 origin이 있다고 나오면:

```bash
git remote set-url origin https://github.com/<본인아이디>/wafer-ai-analyst.git
git push -u origin main
```

## 팀원에게 공유할 설명

```text
GitHub repo 이름은 wafer-ai-analyst로 만들 예정입니다.
이 프로젝트는 반도체 웨이퍼 전기 측정 데이터를 AI가 자동 분석하는 포트폴리오 프로젝트입니다.
원본 데이터는 GitHub에 올리지 않고, parser/feature extraction/anomaly rule/dashboard 코드와 문서만 관리합니다.
```

## 첫 커밋 메시지

추천 첫 커밋:

```text
init wafer ai analyst project
```

