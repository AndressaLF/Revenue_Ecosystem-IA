from __future__ import annotations

import re
from pathlib import Path

import yaml

from shared_components.database.sqlite_repo import Opportunity

RULES_PATH = Path("config/physical_rules.yaml")

SUBREDDIT_PERSONA = {
    "buyitforlife": ("home_consumer", 0.85),
    "homeoffice": ("home_consumer", 0.8),
    "organizationporn": ("home_consumer", 0.75),
    "desksetup": ("home_consumer", 0.8),
}


def load_pain_patterns() -> list[dict]:
    rules = yaml.safe_load(RULES_PATH.read_text(encoding="utf-8"))
    return rules.get("pain_patterns", [])


def extract_pain_category(text: str, patterns: list[dict] | None = None) -> str | None:
    patterns = patterns or load_pain_patterns()
    for item in patterns:
        if re.search(item["regex"], text, re.IGNORECASE):
            return item["category"]
    return None


def classify_persona_from_subreddit(subreddit: str) -> tuple[str, float]:
    key = subreddit.lower().replace("r/", "")
    return SUBREDDIT_PERSONA.get(key, ("home_consumer", 0.55))


def enrich_opportunity_from_text(opp: Opportunity, text: str, subreddit: str = "") -> Opportunity:
    persona, confidence = classify_persona_from_subreddit(subreddit)
    opp.persona_tag = persona
    opp.persona_confidence = confidence
    opp.pain_category = extract_pain_category(text) or opp.pain_category
    if not opp.pain_statement and len(text) <= 200:
        opp.pain_statement = text.strip()
    opp.suggested_channel = "pinterest"
    if opp.pain_category == "physical_pain":
        opp.jtbd_statement = (
            f"When dealing with {opp.pain_category.replace('_', ' ')}, "
            f"I want a practical fix for my desk setup without overspending."
        )
    return opp
