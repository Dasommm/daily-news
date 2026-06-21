# Project Plan

## Current Status

**Phase:** Initial Implementation Complete
**Last Updated:** 2026-06-21

See [PROGRESS.md](./PROGRESS.md) for detailed completion status.

---

## Immediate Next Steps

### User Actions Required

1. **Configure GitHub Secrets** ⏳
   - Navigate to: `Settings > Secrets and variables > Actions`
   - Add `OPENAI_API_KEY` with your OpenAI API key
   - Add `SLACK_WEBHOOK_URL` with your Slack webhook URL

2. **Test the Bot** ⏳
   - Go to `Actions` tab in GitHub repository
   - Select "Daily News Bot" workflow
   - Click "Run workflow" to test manually
   - Verify news appears in Slack channel

3. **Monitor First Automatic Run** ⏳
   - Wait for scheduled run at 7 AM KST
   - Check Actions tab for execution logs
   - Verify Slack message delivery

---

## Completed Enhancements

- [x] **Korean translation + English vocabulary** (2026-06-21)
  - Each news item now shows a Korean translation (🇰🇷) below its English summary
  - Added a "📚 오늘의 영어 표현" section listing 5 useful English
    expressions from the day's news, each with a Korean meaning and example
  - Implemented within the existing single OpenAI call (no extra cost/latency)
  - See PROGRESS.md "Phase 4" for details

---

## Future Enhancements

### Priority 1: High Value, Low Effort

- [ ] **Add more RSS sources**
  - Business news (e.g., Bloomberg, Reuters)
  - Science news (e.g., Ars Technica)
  - Configurable via environment variables or config file

- [ ] **Error notifications**
  - Send Slack notification if bot fails
  - Include error details for debugging

- [ ] **News filtering**
  - Filter by keywords or topics of interest
  - Remove duplicate or similar news items

### Priority 2: Medium Value, Medium Effort

- [ ] **Customizable schedule**
  - Support multiple daily runs (e.g., morning and evening)
  - Weekend schedule options

- [ ] **News persistence**
  - Store sent news to avoid duplicates
  - Historical archive in GitHub or database

- [ ] **Enhanced formatting**
  - Add news source attribution
  - Include publication timestamps
  - Add "Read more" links to original articles

- [ ] **Multi-channel support**
  - Send to multiple Slack channels
  - Different news categories to different channels

### Priority 3: Advanced Features

- [ ] **User preferences**
  - Allow users to customize news categories
  - Support for different languages
  - Adjustable summary length

- [ ] **Analytics dashboard**
  - Track news delivery statistics
  - Monitor popular topics over time
  - API usage tracking

- [ ] **Interactive features**
  - Slack buttons for "Mark as read" or "Save for later"
  - Feedback mechanism (helpful/not helpful)
  - Request more details on specific news

- [ ] **Alternative AI providers**
  - Support for Claude, Gemini, or other LLMs
  - Fallback to alternative providers if primary fails

- [ ] **Email integration** (from original n8n workflow)
  - Send formatted email in addition to Slack
  - Read from Notion database for email recipients
  - Support HTML email templates

### Priority 4: Infrastructure Improvements

- [ ] **Comprehensive testing**
  - Unit tests for core functions
  - Integration tests for API calls
  - Mock tests for external dependencies

- [ ] **Logging improvements**
  - Structured logging (JSON format)
  - Log levels (DEBUG, INFO, WARNING, ERROR)
  - External logging service integration

- [ ] **Configuration management**
  - YAML/JSON config file for settings
  - Separate configs for dev/prod environments

- [ ] **Docker support**
  - Containerize the application
  - Support for local Docker deployment
  - Docker Compose for full stack

- [ ] **Alternative deployment options**
  - AWS Lambda deployment
  - Google Cloud Functions
  - Self-hosted server with systemd

---

## Technical Debt

None currently. Project is new and well-structured.

---

## Blocked Items

None currently. All required resources are available.

---

## Decisions Log

### Why GitHub Actions?
- **Chosen:** GitHub Actions for scheduling
- **Alternatives considered:** AWS Lambda, Google Cloud Scheduler, cron on VPS
- **Reasoning:** Zero cost, simple setup, integrated with repo, no server maintenance

### Why OpenAI GPT-4o-mini?
- **Chosen:** gpt-4o-mini model
- **Alternatives considered:** gpt-4, gpt-3.5-turbo, Claude
- **Reasoning:** Good balance of cost, speed, and quality for summarization tasks

### Why RSS feeds?
- **Chosen:** RSS feeds for news sources
- **Alternatives considered:** News APIs (NewsAPI, etc.), web scraping
- **Reasoning:** Free, reliable, standardized format, no API key management

### Why Slack Webhooks?
- **Chosen:** Incoming Webhooks
- **Alternatives considered:** Slack Bot API, Slack SDK
- **Reasoning:** Simple, no OAuth flow, sufficient for one-way messages

---

## Success Metrics

### Phase 1 (Current) - MVP Success
- ✅ Bot executes successfully
- ⏳ News delivered to Slack daily at 7 AM
- ⏳ Zero manual intervention required after setup

### Phase 2 - Reliability
- 99%+ uptime over 30 days
- Average execution time < 30 seconds
- Zero cost (within GitHub Actions free tier)

### Phase 3 - User Satisfaction
- User finds news summaries useful
- News is relevant and timely
- Summaries are accurate and concise

---

## Notes for Future Developers

### Adding New RSS Sources
1. Add URL to `self.feeds` dictionary in `DailyNewsBot.__init__()`
2. Update prompt in `summarize_news()` to include new category
3. Update `build_slack_blocks()` to format new category
4. Update README.md to document new source

### Changing Schedule
Edit `.github/workflows/daily-news.yml`:
```yaml
schedule:
  - cron: 'MM HH * * *'  # UTC time
```
Remember: KST = UTC + 9

### Debugging GitHub Actions
- Check Actions tab for logs
- Add `set -x` to workflow for verbose output
- Use `workflow_dispatch` for manual testing

### Local Development
Always test locally before pushing:
```bash
cp .env.example .env
# Edit .env with real credentials
python daily_news.py
```

---

## Questions for Stakeholders

- Should we add more news sources? Which ones?
- Is 7 AM KST the best time, or should we offer multiple times?
- Do you want email delivery in addition to Slack?
- Should we track metrics like most-read topics?

---

## Related Documentation

- [README.md](./README.md) - User-facing setup guide
- [PROGRESS.md](./PROGRESS.md) - What's been done
- [CLAUDE.md](./CLAUDE.md) - Instructions for AI agents
