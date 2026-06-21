# Instructions for AI Agents

**⚠️ IMPORTANT: Read this file at the start of every session**

This document provides context and guidelines for AI agents working on the Daily News Bot project.

---

## 🚀 Session Start Checklist

When starting a new session, **ALWAYS** do the following in order:

1. **Read [PROGRESS.md](./PROGRESS.md)** - Understand what has been completed
2. **Read [PLAN.md](./PLAN.md)** - Understand current plans and priorities
3. **Read this file (CLAUDE.md)** - Understand project-specific guidelines
4. **Ask the user** what they want to work on

**Example workflow:**
```
Agent: I've reviewed the project documentation:
- PROGRESS.md shows the bot is fully implemented and pushed to GitHub
- PLAN.md shows the next step is configuring GitHub Secrets
- Current status: Waiting for user to set up secrets for testing

What would you like to work on today?
```

---

## 📋 Project Overview

**Project:** Daily News Bot
**Purpose:** Automatically fetch, summarize, and send news to Slack every day at 9 AM KST
**Repository:** https://github.com/Dasommm/daily-news

### Technology Stack
- **Language:** Python 3.11
- **Key Libraries:** feedparser, openai, requests
- **Automation:** GitHub Actions (scheduled workflows)
- **Integration:** Slack Incoming Webhooks
- **AI:** OpenAI GPT-4o-mini for summarization

### Architecture
```
GitHub Actions (Schedule: 9 AM KST)
  ↓
daily_news.py
  ↓
Fetch RSS feeds → Summarize with OpenAI → Send to Slack
```

---

## 🔐 Security Guidelines

**CRITICAL: This project handles sensitive credentials**

### Secrets Management
- **NEVER** commit actual API keys or webhook URLs
- **ALWAYS** use GitHub Secrets for credentials
- **ALWAYS** add sensitive files to `.gitignore`
- `.env` files must NEVER be committed (already in .gitignore)

### Secret Names
- `OPENAI_API_KEY` - OpenAI API key
- `SLACK_WEBHOOK_URL` - Slack incoming webhook URL

### When Adding New Secrets
1. Update `.env.example` with placeholder
2. Document in README.md setup instructions
3. Update GitHub Actions workflow to pass secret as env var
4. Never use real values in example files

---

## 📁 File Structure

```
daily-news/
├── .github/workflows/
│   └── daily-news.yml          # GitHub Actions workflow (DO NOT BREAK THIS)
├── .gitignore                  # Security critical - don't modify without review
├── .env.example                # Template only - never add real values
├── daily_news.py               # Main bot logic
├── requirements.txt            # Python dependencies with pinned versions
├── news_workflow.json          # Reference: Original n8n workflow (READ-ONLY)
├── README.md                   # User-facing documentation
├── PROGRESS.md                 # What's been completed (UPDATE THIS)
├── PLAN.md                     # Future plans (UPDATE THIS)
└── CLAUDE.md                   # This file
```

---

## 🛠 Development Guidelines

### Before Making Changes
1. Read PROGRESS.md to see what's already done
2. Read PLAN.md to see if your change aligns with the plan
3. Check if similar functionality already exists
4. Consider security implications

### When Modifying Code
- **Test locally first** (if possible)
- **Maintain compatibility** with existing GitHub Actions workflow
- **Update documentation** (README.md, PROGRESS.md, PLAN.md)
- **Keep dependencies minimal** - only add if truly necessary
- **Follow existing code style** - match the patterns in daily_news.py

### When Adding Features
1. Check PLAN.md to see if it's already planned
2. If yes, follow the plan's approach
3. If no, discuss with user first
4. Update PLAN.md with your approach
5. Update PROGRESS.md when complete

### When Fixing Bugs
1. Document the bug in PROGRESS.md under "Known Issues"
2. Fix the bug
3. Update PROGRESS.md to mark as resolved
4. Add notes about the fix for future reference

---

## 🔄 Updating Documentation

### When to Update PROGRESS.md
- Completing a task from PLAN.md
- Discovering or fixing a bug
- Changing project configuration
- Adding or removing dependencies
- Any significant milestone

### When to Update PLAN.md
- Adding new feature ideas
- Reprioritizing tasks
- Marking tasks as blocked or unblocked
- Adding technical decisions
- User provides new requirements

### When to Update README.md
- Changing setup instructions
- Adding/removing features
- Updating configuration options
- Changing schedule or behavior
- Adding troubleshooting tips

---

## ⚙️ GitHub Actions Workflow

**File:** `.github/workflows/daily-news.yml`

### Critical Points
- Scheduled via cron: `0 0 * * *` (UTC) = 9 AM KST
- Requires GitHub Secrets to be set by user
- Uses Python 3.11
- Caches pip dependencies for speed

### Don't Break
- The cron schedule (unless explicitly asked)
- Secret passing to environment variables
- Python version pinning
- Dependency installation steps

### Safe to Modify
- Adding new environment variables
- Adding new steps (testing, notifications, etc.)
- Changing Python version (with testing)
- Adding manual trigger options

---

## 🧪 Testing Approach

### Local Testing
```bash
# User needs to create .env file first
cp .env.example .env
# Edit .env with real credentials

# Run the bot
python daily_news.py
```

### GitHub Actions Testing
- Use manual trigger: `workflow_dispatch`
- Check Actions tab for logs
- Verify Slack message delivery

### Before Pushing Code
- Review security: No secrets in code
- Review `.gitignore`: All sensitive files excluded
- Review changes: Use `git diff` to check what's being committed

---

## 🚨 Common Pitfalls

### 1. GitHub Push Protection
- GitHub will block pushes containing webhook URLs
- Even in `.env.example`, URLs must be clearly fake
- Use placeholders like `YOUR_WEBHOOK_URL`, not realistic-looking URLs

### 2. Timezone Confusion
- Cron in GitHub Actions runs in UTC
- Korea (KST) = UTC + 9
- 9 AM KST = 12 AM (00:00) UTC same day = `0 0 * * *`
- Note: GitHub Actions scheduled runs are best-effort and may be delayed by minutes to hours

### 3. Secrets Not Set
- Workflow will fail if GitHub Secrets aren't configured
- This is user's responsibility, not a code bug
- Document clearly in README.md

### 4. API Rate Limits
- OpenAI has rate limits
- RSS feeds can be rate limited
- Add error handling and retries if needed

---

## 💡 AI Agent Best Practices

### Reading Code
- Start with `daily_news.py` - it's well-documented
- Check `news_workflow.json` for original n8n design intent
- GitHub Actions workflow is in `.github/workflows/daily-news.yml`

### Suggesting Changes
- Always explain WHY, not just WHAT
- Consider backward compatibility
- Think about user experience
- Estimate complexity (use PLAN.md priorities as guide)

### Handling User Requests
1. Check if it's already in PLAN.md
2. If yes: "I see this is Priority X in PLAN.md. Let me implement it."
3. If no: "This isn't in the current plan. Let me add it and we can prioritize."

### Debugging Issues
1. Check GitHub Actions logs (if workflow fails)
2. Check for missing GitHub Secrets
3. Check for API errors (OpenAI, Slack, RSS)
4. Verify timezone/schedule issues

---

## 📞 Communication Style

### With Users
- Be clear about what's already done (reference PROGRESS.md)
- Explain tradeoffs when suggesting alternatives
- Ask for confirmation before major changes
- Provide clear next steps

### In Documentation
- Keep PROGRESS.md factual and chronological
- Keep PLAN.md organized by priority
- Use checkboxes for trackable items
- Include dates for time-sensitive information

---

## 🎯 Project Goals

### Primary Goal
Deliver relevant, summarized news to Slack every morning at 9 AM KST without manual intervention.

### Secondary Goals
- Maintain zero cost (GitHub Actions free tier)
- Ensure security of API keys and webhooks
- Keep codebase simple and maintainable
- Provide clear documentation for setup

### Non-Goals (for now)
- Complex user interfaces
- Real-time news updates
- Advanced analytics or dashboards
- Multi-user support with preferences

---

## 🔗 Important Links

- **Repository:** https://github.com/Dasommm/daily-news
- **OpenAI API:** https://platform.openai.com/api-keys
- **Slack Webhooks:** https://api.slack.com/messaging/webhooks
- **GitHub Actions:** https://docs.github.com/actions
- **Cron Helper:** https://crontab.guru/

---

## 📝 Template for New Sessions

When starting a new session, use this template:

```markdown
I've reviewed the project context:

**Completed:**
- [Key points from PROGRESS.md]

**Current Status:**
- [Latest status from PROGRESS.md]

**Next Planned:**
- [Top items from PLAN.md]

What would you like to work on?
```

---

## 🤝 Contributing to This Project

### Adding New Features
1. Add to PLAN.md with priority
2. Implement with tests (if applicable)
3. Update README.md if user-facing
4. Update PROGRESS.md when done
5. Commit with clear message

### Improving Documentation
- These files (PROGRESS.md, PLAN.md, CLAUDE.md) are living documents
- Update them as the project evolves
- Keep them in sync with reality
- Remove outdated information

---

**Last Updated:** 2026-03-18

**Version:** 1.0.0

---

## Remember

> "The best code is well-documented code that future you (or another agent) can understand six months later."

Always read PROGRESS.md and PLAN.md at the start of each session. They are your roadmap.
