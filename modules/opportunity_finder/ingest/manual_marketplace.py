from __future__ import annotations

import json
from pathlib import Path

import yaml

from modules.opportunity_finder.filter.rules import classify_intent, load_physical_rules
from modules.opportunity_finder.score.physical_scoring import estimate_epc
from shared_components.database.sqlite_repo import Opportunity, OpportunityRepository

PROGRAMS_PATH = Path("config/affiliate_programs.yaml")


def load_programs() -> dict:
    data = yaml.safe_load(PROGRAMS_PATH.read_text(encoding="utf-8"))
    return {p["name"]: p for p in data.get("programs", [])}


def load_program_by_platform(platform: str) -> dict:
    mapping = {
        "amazon": "amazon_associates",
        "digistore24": "digistore24",
        "clickbank": "clickbank",
    }
    key = mapping.get(platform.lower())
    if not key:
        raise ValueError(f"Unknown platform: {platform}")
    programs = load_programs()
    if key not in programs:
        raise ValueError(f"Program not configured: {key}")
    return programs[key]


def import_affiliate_manual(
    repo: OpportunityRepository,
    platform: str,
    keyword: str,
    product_name: str,
    price: float,
    affiliate_url: str,
    commission_pct: float | None = None,
    cookie_days: int | None = None,
    refund_rate: float | None = None,
    gravity: float | None = None,
    rating: float | None = None,
    reviews: int | None = None,
    vendor_id: str | None = None,
) -> str:
    """Import opportunity from human research (Digistore24, ClickBank, Amazon)."""
    program = load_program_by_platform(platform)
    vertical = program["vertical"]
    source = f"{platform}:manual"

    commission = commission_pct if commission_pct is not None else program["commission_pct_default"]
    cookie = cookie_days if cookie_days is not None else program["cookie_days"]
    refund = refund_rate if refund_rate is not None else 0.03
    conv = program.get("conv_rate_est", 0.02)

    if platform == "amazon":
        rules = load_physical_rules()
        intent_patterns = rules.get("intent_patterns", [])
    else:
        intent_patterns = ["review", "worth it", "best .+ for", "program", "course"]

    intent = classify_intent(keyword, intent_patterns)
    epc = estimate_epc(price, commission, conv, refund)

    raw = {
        "platform": platform,
        "product_name": product_name,
        "price": price,
        "commission_pct": commission,
        "cookie_days": cookie,
        "refund_rate": refund,
        "gravity": gravity,
        "rating": rating,
        "reviews": reviews,
        "vendor_id": vendor_id,
        "program": program["name"],
    }

    opp_id = repo.new_id(keyword, source)
    channel = program.get("funnel", "").split("→")[0].strip().lower()
    if "pinterest" in channel:
        suggested = "pinterest"
    elif "youtube" in program.get("funnel", "").lower():
        suggested = "youtube"
    else:
        suggested = "medium"

    opp = Opportunity(
        id=opp_id,
        source=source,
        keyword=keyword,
        vertical=vertical,
        product_name=product_name,
        affiliate_url=affiliate_url,
        raw_data=json.dumps(raw, ensure_ascii=False),
        estimated_price=price,
        commission_pct=commission,
        cookie_days=cookie,
        refund_rate=refund,
        estimated_epc=epc,
        intent_score=max(intent, 0.35),
        search_volume=2500 if vertical == "digital" else 3000,
        competition_score=28.0,
        persona_tag="home_consumer" if vertical == "physical" else "creator",
        persona_confidence=0.65,
        suggested_channel=suggested,
        enrichment_source=json.dumps({"human": platform, "nomad_payout": True}),
        status="PENDING",
    )

    # ClickBank gravity gate
    if platform == "clickbank" and gravity is not None:
        gmin = program.get("filters_human", {}).get("gravity_min", 20)
        if gravity < gmin:
            opp.status = "REJECTED"
            opp.reject_reason = f"low_gravity:{gravity}"

    # Amazon social proof gate
    if platform == "amazon" and rating is not None and reviews is not None:
        rules = load_physical_rules()
        if rating < rules["validation"]["rating_min"] or reviews < rules["validation"]["reviews_min"]:
            opp.status = "REJECTED"
            opp.reject_reason = "low_social_proof"

    # Digital EPC gate (humano já filtrou; validação leve)
    if vertical == "digital" and epc < 0.25:
        opp.status = "REJECTED"
        opp.reject_reason = f"low_epc:{epc}"

    repo.upsert(opp)
    return opp_id


def import_amazon_manual(
    repo: OpportunityRepository,
    keyword: str,
    product_name: str,
    price: float,
    affiliate_url: str,
    rating: float = 4.5,
    reviews: int = 200,
) -> str:
    return import_affiliate_manual(
        repo,
        platform="amazon",
        keyword=keyword,
        product_name=product_name,
        price=price,
        affiliate_url=affiliate_url,
        rating=rating,
        reviews=reviews,
    )
