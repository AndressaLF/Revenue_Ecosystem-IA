from __future__ import annotations

from modules.opportunity_finder.score.physical_scoring import estimate_epc, score_physical
from modules.opportunity_finder.filter.rules import load_physical_rules
from shared_components.database.sqlite_repo import Opportunity


def test_estimate_epc_amazon_typical():
    # $50 * 3% * 8% conv * (1-3% refund) ≈ $0.116 - need higher price for $0.40 EPC
    epc = estimate_epc(75.0, 3.0, 0.08, 0.03)
    assert epc >= 0.17


def test_physical_validated_threshold():
    rules = load_physical_rules()
    opp = Opportunity(
        id="test1",
        source="test",
        keyword="best cable management tray for small desk",
        vertical="physical",
        estimated_price=49.0,
        intent_score=0.7,
        search_volume=3000,
        competition_score=25.0,
        pain_category="organization",
    )
    scored = score_physical(opp, rules)
    assert scored.estimated_epc > 0
    assert scored.matrix_score > 0
