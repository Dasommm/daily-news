# 📰 Daily News Bot

매일 오전 7시에 세계 뉴스와 기술 뉴스를 수집하여 요약한 후 Slack으로 전달하는 자동화 봇입니다.

## ✨ 특징

- **자동 뉴스 수집**: RSS 피드에서 최신 뉴스 자동 수집
  - 🌍 세계 뉴스 (BBC World News)
  - 💻 기술 뉴스 (The Verge)
- **AI 요약**: OpenAI GPT-4를 사용한 스마트 뉴스 요약
- **한국어 번역**: 각 뉴스의 영어 요약과 함께 한국어 번역(🇰🇷)을 제공
- **오늘의 영어 표현**: 그날 뉴스에서 뽑은 알아두면 좋을 영어 단어·표현 5개를 뜻과 예문과 함께 메시지 하단에 정리 (📚)
- **Slack 통합**: 깔끔한 Block Kit 형식으로 Slack 메시지 전송
- **자동 실행**: GitHub Actions를 통한 매일 자동 실행
- **보안**: GitHub Secrets를 통한 안전한 API 키 관리

## 🚀 설정 방법

### 1. 저장소 클론

```bash
git clone https://github.com/Dasommm/daily-news.git
cd daily-news
```

### 2. GitHub Secrets 설정

저장소 Settings > Secrets and variables > Actions > New repository secret에서 다음 2개의 시크릿을 추가합니다:

#### `OPENAI_API_KEY`
1. [OpenAI Platform](https://platform.openai.com/api-keys)에서 API 키 생성
2. Secret name: `OPENAI_API_KEY`
3. Secret value: 생성한 API 키 입력

#### `SLACK_WEBHOOK_URL`
1. Slack 워크스페이스 설정 > 앱 관리 > Incoming Webhooks 검색 및 추가
2. 뉴스를 받을 채널 선택
3. Webhook URL 복사
4. Secret name: `SLACK_WEBHOOK_URL`
5. Secret value: 복사한 Webhook URL 입력

### 3. GitHub Actions 활성화

- 저장소에 코드를 푸시하면 자동으로 활성화됩니다
- Actions 탭에서 워크플로우 실행 상태를 확인할 수 있습니다

### 4. 수동 실행 (테스트용)

GitHub Actions 탭에서 "Daily News Bot" 워크플로우를 선택하고 "Run workflow" 버튼을 클릭하여 즉시 실행할 수 있습니다.

## 🧪 로컬 테스트

로컬 환경에서 테스트하려면:

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 파일 생성
cp .env.example .env

# .env 파일을 열어 실제 API 키와 Webhook URL 입력
# OPENAI_API_KEY=your_actual_key
# SLACK_WEBHOOK_URL=your_actual_webhook_url

# 스크립트 실행
python daily_news.py
```

## ⏰ 실행 시간 변경

기본 실행 시간은 매일 오전 7시(KST)입니다. 변경하려면:

`.github/workflows/daily-news.yml` 파일에서 cron 표현식을 수정합니다:

```yaml
schedule:
  - cron: '0 22 * * *'  # UTC 22:00 = KST 07:00
```

**시간대 참고:**
- KST(한국 표준시) = UTC + 9
- 예: KST 오전 9시 = UTC 0시 → `'0 0 * * *'`
- Cron 표현식: [Crontab Guru](https://crontab.guru/) 참고

## 📁 프로젝트 구조

```
daily-news/
├── .github/
│   └── workflows/
│       └── daily-news.yml      # GitHub Actions 워크플로우
├── .gitignore                  # Git 제외 파일 목록
├── .env.example                # 환경 변수 템플릿
├── daily_news.py               # 메인 봇 스크립트
├── requirements.txt            # Python 의존성
├── news_workflow.json          # n8n 워크플로우 참고 (원본)
├── README.md                   # 프로젝트 문서 (이 파일)
├── CLAUDE.md                   # AI 에이전트를 위한 지침
├── PROGRESS.md                 # 작업 진행 상황 기록
└── PLAN.md                     # 향후 계획 및 로드맵
```

## 📚 문서

이 프로젝트는 여러 문서로 구성되어 있습니다:

- **[README.md](./README.md)** - 프로젝트 개요 및 설정 가이드 (이 파일)
- **[CLAUDE.md](./CLAUDE.md)** - AI 에이전트를 위한 작업 지침
- **[PROGRESS.md](./PROGRESS.md)** - 완료된 작업 및 현재 상태
- **[PLAN.md](./PLAN.md)** - 향후 개선 사항 및 로드맵

새로운 세션을 시작하거나 프로젝트 기여 시 CLAUDE.md를 먼저 읽어주세요.

## 🔒 보안 주의사항

- ⚠️ **절대로** `.env` 파일을 Git에 커밋하지 마세요
- ⚠️ API 키와 Webhook URL을 코드에 직접 하드코딩하지 마세요
- ⚠️ GitHub Secrets를 사용하여 민감 정보를 안전하게 관리하세요
- `.gitignore`에 `.env` 파일이 포함되어 있는지 확인하세요

## 🛠 기술 스택

- **Python 3.11**
- **OpenAI API** - GPT-4 기반 뉴스 요약
- **Slack Incoming Webhooks** - 메시지 전송
- **GitHub Actions** - 자동화 및 스케줄링
- **feedparser** - RSS 피드 파싱

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 풀 리퀘스트는 언제나 환영합니다!
