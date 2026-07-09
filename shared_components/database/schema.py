from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path("storage/local_cache.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    keyword TEXT NOT NULL,
    vertical TEXT NOT NULL,
    product_name TEXT,
    affiliate_url TEXT,
    raw_data TEXT,
    search_volume INTEGER DEFAULT 0,
    competition_score REAL DEFAULT 0.0,
    trend_velocity REAL DEFAULT 0.0,
    intent_score REAL DEFAULT 0.0,
    persona_tag TEXT,
    persona_confidence REAL DEFAULT 0.0,
    persona_signals TEXT,
    pain_statement TEXT,
    pain_category TEXT,
    pain_urgency_score REAL DEFAULT 0.0,
    jtbd_statement TEXT,
    suggested_channel TEXT,
    estimated_price REAL DEFAULT 0.0,
    commission_pct REAL DEFAULT 0.0,
    cookie_days INTEGER DEFAULT 0,
    estimated_epc REAL DEFAULT 0.0,
    fci_score REAL,
    iema_score REAL,
    matrix_score REAL DEFAULT 0.0,
    friction_score INTEGER DEFAULT 3,
    lp_quality_score INTEGER DEFAULT 3,
    churn_monthly REAL,
    arpu_monthly REAL,
    refund_rate REAL,
    opportunity_score REAL DEFAULT 0.0,
    ai_score REAL DEFAULT 0.0,
    status TEXT DEFAULT 'PENDING',
    reject_reason TEXT,
    enrichment_source TEXT,
    last_enriched_at TIMESTAMP,
    produced_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pain_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    source_url TEXT,
    raw_text TEXT NOT NULL,
    pain_category TEXT,
    persona_hint TEXT,
    engagement_score INTEGER DEFAULT 0,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    opportunity_id TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
);

CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id TEXT NOT NULL,
    channel TEXT NOT NULL,
    views INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    revenue_usd REAL DEFAULT 0.0,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
);
"""


def init_db(db_path: Path | None = None) -> Path:
    path = db_path or DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.executescript(SCHEMA_SQL)
    return path


def make_opportunity_id(keyword: str, source: str) -> str:
    digest = hashlib.sha256(f"{keyword}:{source}".encode()).hexdigest()
    return digest[:16]
