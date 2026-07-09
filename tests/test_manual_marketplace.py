from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from modules.opportunity_finder.ingest.manual_marketplace import import_affiliate_manual
from shared_components.database.schema import init_db
from shared_components.database.sqlite_repo import OpportunityRepository


@pytest.fixture
def repo(tmp_path: Path) -> OpportunityRepository:
    db = tmp_path / "test.db"
    init_db(db)
    return OpportunityRepository(db)


def test_import_clickbank_rejects_low_gravity(repo: OpportunityRepository) -> None:
    oid = import_affiliate_manual(
        repo,
        platform="clickbank",
        keyword="weight loss program review",
        product_name="Test CB Product",
        price=47.0,
        affiliate_url="https://hop.clickbank.net/?affiliate=x&vendor=y",
        gravity=10,
        commission_pct=50,
    )
    opp = repo.get(oid)
    assert opp is not None
    assert opp.status == "REJECTED"
    assert opp.reject_reason == "low_gravity:10"


def test_import_digistore24_pending(repo: OpportunityRepository) -> None:
    oid = import_affiliate_manual(
        repo,
        platform="digistore24",
        keyword="business course review worth it",
        product_name="DS24 Product",
        price=97.0,
        affiliate_url="https://www.digistore24.com/redir/test",
        commission_pct=25,
    )
    opp = repo.get(oid)
    assert opp is not None
    assert opp.vertical == "digital"
    assert opp.cookie_days == 180
    assert opp.estimated_epc >= 0.25
