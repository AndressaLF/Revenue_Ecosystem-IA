from __future__ import annotations

from shared_components.database.sqlite_repo import Opportunity


def estimate_epc(price: float, commission_pct: float, conv_rate: float, refund_rate: float) -> float:
    """EPC per click to Amazon (simplified)."""
    net_commission = price * (commission_pct / 100.0) * (1.0 - refund_rate)
    return round(net_commission * conv_rate, 4)


def matrix_score_physical(opp: Opportunity) -> float:
    """Weighted 0-100 matrix from playbook physical_products.md (simplified)."""
    components = [
        (opp.intent_score * 10, 1.5),  # demanda transacional
        ((100 - opp.competition_score) / 10, 1.5),  # concorrência inversa
        (min(opp.estimated_epc / 0.5, 1.0) * 10, 1.2),  # margem/EPC proxy
        (6.0, 1.2),  # conversão LP placeholder até humano testar
        (8.0 if 35 <= opp.estimated_price <= 75 else 5.0, 1.0),
        (7.0 if opp.pain_category in {"physical_pain", "organization"} else 5.0, 1.0),
        (5.0, 0.8),  # cookie curto Amazon — penalizado vs SaaS
        (8.0 if (opp.refund_rate or 0) < 0.04 else 4.0, 0.8),
        (8.0, 0.6),  # potencial visual Pinterest
        (7.0, 0.4),  # efeito carrinho esperado
    ]
    total_weight = sum(w for _, w in components)
    weighted = sum(score * w for score, w in components)
    return round((weighted / total_weight) * 10, 2)


def opportunity_score(opp: Opportunity) -> float:
    return round(
        opp.intent_score * 30
        + min(opp.search_volume / 10000, 1.0) * 25
        + (100 - opp.competition_score) * 0.2
        + min(opp.estimated_epc / 1.0, 1.0) * 15
        + (opp.matrix_score / 100) * 10,
        2,
    )


def score_physical(opp: Opportunity, rules: dict) -> Opportunity:
    amazon = rules["amazon"]
    refund = opp.refund_rate or 0.03
    opp.commission_pct = opp.commission_pct or amazon["commission_pct_default"]
    opp.cookie_days = amazon["cookie_days"]
    opp.estimated_epc = estimate_epc(
        opp.estimated_price or 50.0,
        opp.commission_pct,
        amazon["conversion_rate_est"],
        refund,
    )
    opp.refund_rate = refund
    opp.matrix_score = matrix_score_physical(opp)
    opp.opportunity_score = opportunity_score(opp)

    validation = rules["validation"]
    if (
        opp.opportunity_score >= validation["opportunity_score_min"]
        and opp.matrix_score >= validation["matrix_score_min"]
        and opp.estimated_epc >= validation["estimated_epc_min"]
    ):
        opp.status = "VALIDATED"
        opp.reject_reason = None
    else:
        opp.status = "REJECTED"
        reasons = []
        if opp.opportunity_score < validation["opportunity_score_min"]:
            reasons.append("low_opportunity_score")
        if opp.matrix_score < validation["matrix_score_min"]:
            reasons.append("low_matrix_score")
        if opp.estimated_epc < validation["estimated_epc_min"]:
            reasons.append("low_epc")
        opp.reject_reason = ",".join(reasons)
    return opp
