#!/usr/bin/env python3
"""
Daily News Bot - Fetches and summarizes news from RSS feeds and sends to Slack
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict
import feedparser
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file (for local testing)
load_dotenv()


class DailyNewsBot:
    """Main bot class for fetching, summarizing, and sending news"""

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

        # Validate environment variables
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        if not self.slack_webhook_url:
            raise ValueError("SLACK_WEBHOOK_URL environment variable is required")

        self.client = OpenAI(api_key=self.openai_api_key)

        # RSS feed sources
        self.feeds = {
            "tech": "https://www.theverge.com/rss/index.xml",
            "world": "https://feeds.bbci.co.uk/news/world/rss.xml"
        }

    def fetch_rss_feed(self, feed_url: str, limit: int = 10) -> List[Dict]:
        """Fetch and parse RSS feed"""
        try:
            feed = feedparser.parse(feed_url)
            entries = []

            for entry in feed.entries[:limit]:
                entries.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", "")
                })

            return entries
        except Exception as e:
            print(f"Error fetching RSS feed {feed_url}: {e}")
            return []

    def summarize_news(self, tech_entries: List[Dict], world_entries: List[Dict]) -> Dict:
        """Use OpenAI to summarize news entries"""

        # Prepare context for AI
        tech_context = "\n\n".join([
            f"Title: {entry['title']}\nSummary: {entry['summary'][:200]}"
            for entry in tech_entries
        ])

        world_context = "\n\n".join([
            f"Title: {entry['title']}\nSummary: {entry['summary'][:200]}"
            for entry in world_entries
        ])

        today = datetime.now().strftime("%Y-%m-%d")

        prompt = f"""Summarize world news and tech news from the last 24 hours. Skip your comments.
Today is {today}.

Tech News Context:
{tech_context}

World News Context:
{world_context}

Please provide a JSON response with the following structure:
{{
  "date": "{today}",
  "world_news": [
    {{
      "headline": "Brief headline",
      "summary": "2-3 sentence summary in English",
      "summary_ko": "Korean translation of the English summary"
    }}
  ],
  "tech_news": [
    {{
      "headline": "Brief headline",
      "summary": "2-3 sentence summary in English",
      "summary_ko": "Korean translation of the English summary"
    }}
  ],
  "vocabulary": [
    {{
      "expression": "Useful English word or expression that appears in today's news",
      "meaning": "Korean meaning of the expression",
      "example": "A short English example sentence using the expression",
      "example_ko": "Korean translation of the example sentence"
    }}
  ]
}}

Provide 3-5 items for each news category. Make headlines concise and summaries informative.
For each news item, write the summary in English and provide a natural Korean translation in summary_ko.
For vocabulary, select exactly 5 useful English words or expressions drawn from across all of today's news (both world and tech) that a Korean learner would benefit from knowing. For each, provide an English example sentence and its natural Korean translation in example_ko."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional news summarizer and English tutor for Korean readers. Provide concise, informative summaries with Korean translations in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            print(f"Error summarizing news with OpenAI: {e}")
            raise

    def build_slack_blocks(self, news_data: Dict) -> List[Dict]:
        """Build Slack Block Kit message"""
        blocks = []

        # Header
        blocks.append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📰 Daily News Brief 📰"
            }
        })

        # Date context
        date_str = news_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        blocks.append({
            "type": "context",
            "elements": [{
                "type": "mrkdwn",
                "text": f"*{date_str}* | Daily News Summary"
            }]
        })

        blocks.append({"type": "divider"})

        # World News
        blocks.append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🌍 World News"
            }
        })

        for news_item in news_data.get("world_news", []):
            headline = news_item.get("headline", "")
            summary = news_item.get("summary", "")
            summary_ko = news_item.get("summary_ko", "")
            text = f"✔️ *{headline}*\n\n{summary}"
            if summary_ko:
                text += f"\n🇰🇷 {summary_ko}"
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            })

        blocks.append({"type": "divider"})

        # Tech News
        blocks.append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "💻 Tech News"
            }
        })

        for news_item in news_data.get("tech_news", []):
            headline = news_item.get("headline", "")
            summary = news_item.get("summary", "")
            summary_ko = news_item.get("summary_ko", "")
            text = f"☑️ *{headline}*\n\n{summary}"
            if summary_ko:
                text += f"\n🇰🇷 {summary_ko}"
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            })

        blocks.append({"type": "divider"})

        # Today's English Expressions
        vocabulary = news_data.get("vocabulary", [])
        if vocabulary:
            blocks.append({
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📚 오늘의 영어 표현"
                }
            })

            vocab_lines = []
            for idx, item in enumerate(vocabulary, start=1):
                expression = item.get("expression", "")
                meaning = item.get("meaning", "")
                example = item.get("example", "")
                example_ko = item.get("example_ko", "")
                line = f"{idx}. *{expression}* — {meaning}"
                if example:
                    line += f"\n   예: {example}"
                    if example_ko:
                        line += f"\n   ({example_ko})"
                vocab_lines.append(line)

            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n\n".join(vocab_lines)
                }
            })

            blocks.append({"type": "divider"})

        return blocks

    def send_to_slack(self, blocks: List[Dict]) -> bool:
        """Send message to Slack via webhook"""
        try:
            payload = {"blocks": blocks}
            response = requests.post(
                self.slack_webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            print("✅ Successfully sent message to Slack")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending message to Slack: {e}")
            return False

    def run(self):
        """Main execution flow"""
        print("🚀 Starting Daily News Bot...")

        # Fetch RSS feeds
        print("📡 Fetching RSS feeds...")
        tech_entries = self.fetch_rss_feed(self.feeds["tech"])
        world_entries = self.fetch_rss_feed(self.feeds["world"])

        print(f"  - Tech news: {len(tech_entries)} entries")
        print(f"  - World news: {len(world_entries)} entries")

        if not tech_entries and not world_entries:
            print("❌ No news entries found")
            return False

        # Summarize with OpenAI
        print("🤖 Summarizing news with OpenAI...")
        news_summary = self.summarize_news(tech_entries, world_entries)

        # Build Slack message
        print("📝 Building Slack message...")
        slack_blocks = self.build_slack_blocks(news_summary)

        # Send to Slack
        print("📤 Sending to Slack...")
        success = self.send_to_slack(slack_blocks)

        if success:
            print("✅ Daily news bot completed successfully!")
        else:
            print("❌ Failed to send news to Slack")
            return False

        return True


def main():
    """Entry point"""
    try:
        bot = DailyNewsBot()
        success = bot.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
