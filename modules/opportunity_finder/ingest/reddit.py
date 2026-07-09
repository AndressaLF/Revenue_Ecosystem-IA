from __future__ import annotations

import json

import httpx

from modules.opportunity_finder.audience.pain_extractor import (
    enrich_opportunity_from_text,
    extract_pain_category,
)
from modules.opportunity_finder.filter.rules import classify_intent, load_physical_rules
from shared_components.database.sqlite_repo import Opportunity, OpportunityRepository

REDDIT_BASE = "https://www.reddit.com"


def fetch_subreddit_posts(subreddit: str, limit: int = 15) -> list[dict]:
    url = f"{REDDIT_BASE}/r/{subreddit}/hot.json?limit={limit}"
    headers = {"User-Agent": "RE-IA/0.1 (physical research bot; docs in README)"}
    with httpx.Client(timeout=30.0, headers=headers) as client:
        resp = client.get(url)
        resp.raise_for_status()
        payload = resp.json()
    posts = []
    for child in payload.get("data", {}).get("children", []):
        data = child.get("data", {})
        posts.append(
            {
                "subreddit": subreddit,
                "title": data.get("title", ""),
                "url": f"{REDDIT_BASE}{data.get('permalink', '')}",
                "score": int(data.get("score", 0)),
                "num_comments": int(data.get("num_comments", 0)),
            }
        )
    return posts


def ingest_reddit_physical(repo: OpportunityRepository) -> int:
    rules = load_physical_rules()
    intent_patterns = rules.get("intent_patterns", [])
    count = 0
    for subreddit in rules.get("subreddits", []):
        try:
            posts = fetch_subreddit_posts(subreddit)
        except httpx.HTTPError:
            continue
        for post in posts:
            title = post["title"]
            pain = extract_pain_category(title)
            if not pain and classify_intent(title, intent_patterns) < 0.25:
                continue
            keyword = title[:120]
            source = f"reddit:{subreddit}"
            opp_id = repo.new_id(keyword, source)
            engagement = post["score"] + post["num_comments"]
            urgency = 0.25 if engagement >= 30 else 0.0
            opp = Opportunity(
                id=opp_id,
                source=source,
                keyword=keyword,
                vertical="physical",
                raw_data=json.dumps(post, ensure_ascii=False),
                intent_score=classify_intent(keyword, intent_patterns),
                pain_category=pain,
                pain_urgency_score=urgency,
                search_volume=1500,
                competition_score=35.0,
            )
            opp = enrich_opportunity_from_text(opp, title, subreddit)
            repo.upsert(opp)
            repo.insert_pain_signal(
                source="reddit",
                raw_text=title,
                source_url=post["url"],
                pain_category=pain,
                persona_hint=opp.persona_tag,
                engagement_score=engagement,
                opportunity_id=opp_id,
            )
            count += 1
    return count
