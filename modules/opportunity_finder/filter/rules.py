from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

RULES_PATH = Path("config/physical_rules.yaml")


def load_physical_rules() -> dict:
    with RULES_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def classify_intent(keyword: str, patterns: list[str]) -> float:
    text = keyword.lower()
    score = 0.0
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            score += 0.35
    generic = re.search(r"\b(tips|how to)\b", text) and not re.search(
        r"\b(best|worth|for)\b", text
    )
    if generic:
        score -= 0.4
    return max(0.0, min(1.0, score))


def apply_physical_filters(opp, rules: dict) -> tuple[bool, str | None]:
    price = opp.estimated_price
    pmin = rules["price"]["min"]
    pmax = rules["price"]["max"]

    if price and (price < pmin or price > pmax):
        return False, f"price_out_of_zone:{price}"

    if opp.search_volume and opp.search_volume < rules["validation"]["search_volume_min"]:
        return False, "low_search_volume"

    if opp.competition_score > rules["validation"]["competition_score_max"]:
        return False, "high_competition"

    if opp.refund_rate and opp.refund_rate > rules["amazon"]["refund_rate_max"]:
        return False, "high_refund_rate"

    if opp.intent_score < 0.25:
        return False, "low_intent"

    return True, None
