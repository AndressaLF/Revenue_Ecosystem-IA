from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from shared_components.database.schema import DEFAULT_DB_PATH, make_opportunity_id


@dataclass
class Opportunity:
    id: str
    source: str
    keyword: str
    vertical: str = "physical"
    product_name: str | None = None
    affiliate_url: str | None = None
    raw_data: str | None = None
    search_volume: int = 0
    competition_score: float = 0.0
    trend_velocity: float = 0.0
    intent_score: float = 0.0
    persona_tag: str | None = None
    persona_confidence: float = 0.0
    pain_statement: str | None = None
    pain_category: str | None = None
    pain_urgency_score: float = 0.0
    jtbd_statement: str | None = None
    suggested_channel: str | None = None
    estimated_price: float = 0.0
    commission_pct: float = 3.0
    cookie_days: int = 24
    estimated_epc: float = 0.0
    matrix_score: float = 0.0
    refund_rate: float = 0.0
    opportunity_score: float = 0.0
    status: str = "PENDING"
    reject_reason: str | None = None
    enrichment_source: str | None = None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Opportunity":
        data = dict(row)
        return cls(**{k: data[k] for k in data if k in cls.__dataclass_fields__})


class OpportunityRepository:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or DEFAULT_DB_PATH

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def upsert(self, opp: Opportunity) -> None:
        fields = asdict(opp)
        columns = ", ".join(fields.keys())
        placeholders = ", ".join(f":{k}" for k in fields.keys())
        updates = ", ".join(f"{k}=excluded.{k}" for k in fields if k != "id")
        sql = f"""
            INSERT INTO opportunities ({columns}) VALUES ({placeholders})
            ON CONFLICT(id) DO UPDATE SET {updates},
                updated_at = CURRENT_TIMESTAMP
        """
        with self._connect() as conn:
            conn.execute(sql, fields)
            conn.commit()

    def list_by_status(self, status: str, vertical: str | None = None) -> list[Opportunity]:
        sql = "SELECT * FROM opportunities WHERE status = ?"
        params: list[Any] = [status]
        if vertical:
            sql += " AND vertical = ?"
            params.append(vertical)
        sql += " ORDER BY opportunity_score DESC, estimated_epc DESC"
        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [Opportunity.from_row(r) for r in rows]

    def get(self, opportunity_id: str) -> Opportunity | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM opportunities WHERE id = ?", (opportunity_id,)
            ).fetchone()
        return Opportunity.from_row(row) if row else None

    def update_status(
        self, opportunity_id: str, status: str, reject_reason: str | None = None
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE opportunities
                SET status = ?, reject_reason = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (status, reject_reason, opportunity_id),
            )
            conn.commit()

    def insert_pain_signal(
        self,
        source: str,
        raw_text: str,
        source_url: str | None = None,
        pain_category: str | None = None,
        persona_hint: str | None = None,
        engagement_score: int = 0,
        opportunity_id: str | None = None,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO pain_signals
                (source, source_url, raw_text, pain_category, persona_hint,
                 engagement_score, opportunity_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source,
                    source_url,
                    raw_text,
                    pain_category,
                    persona_hint,
                    engagement_score,
                    opportunity_id,
                ),
            )
            conn.commit()

    @staticmethod
    def new_id(keyword: str, source: str) -> str:
        return make_opportunity_id(keyword, source)

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def export_json(self, opportunity_id: str) -> dict[str, Any]:
        opp = self.get(opportunity_id)
        if not opp:
            raise ValueError(f"Opportunity not found: {opportunity_id}")
        return asdict(opp)
