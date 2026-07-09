from __future__ import annotations

import json
from pathlib import Path

import typer

from modules.opportunity_finder.filter.rules import (
    apply_physical_filters,
    classify_intent,
    load_physical_rules,
)
from modules.opportunity_finder.ingest.manual_marketplace import (
    import_affiliate_manual,
    import_amazon_manual,
)
from modules.opportunity_finder.ingest.reddit import ingest_reddit_physical
from modules.opportunity_finder.score.physical_scoring import score_physical
from shared_components.database.schema import init_db
from shared_components.database.sqlite_repo import Opportunity, OpportunityRepository

app = typer.Typer(help="RE-IA opportunity finder — physical vertical MVP")


@app.callback()
def _init() -> None:
    init_db()


@app.command("ingest")
def ingest(
    source: str = typer.Option("reddit", help="Comma-separated: reddit"),
) -> None:
    repo = OpportunityRepository()
    total = 0
    if "reddit" in source:
        total += ingest_reddit_physical(repo)
    typer.echo(f"Ingested {total} physical opportunities")


@app.command("import-amazon")
def import_amazon(
    keyword: str = typer.Option(...),
    product_name: str = typer.Option(...),
    price: float = typer.Option(...),
    affiliate_url: str = typer.Option(...),
    rating: float = typer.Option(4.5),
    reviews: int = typer.Option(200),
) -> None:
    repo = OpportunityRepository()
    opp_id = import_amazon_manual(
        repo, keyword, product_name, price, affiliate_url, rating, reviews
    )
    typer.echo(f"Imported Amazon opportunity: {opp_id}")


@app.command("import-affiliate")
def import_affiliate(
    platform: str = typer.Option(
        ...,
        help="amazon | digistore24 | clickbank",
    ),
    keyword: str = typer.Option(..., help="SEO / review keyword EN"),
    product_name: str = typer.Option(...),
    price: float = typer.Option(..., help="Price or avg $/sale"),
    affiliate_url: str = typer.Option(..., help="Hoplink or Amazon URL"),
    commission_pct: float | None = typer.Option(None),
    cookie_days: int | None = typer.Option(None),
    refund_rate: float | None = typer.Option(None),
    gravity: float | None = typer.Option(None, help="ClickBank gravity"),
    rating: float | None = typer.Option(None, help="Amazon only"),
    reviews: int | None = typer.Option(None, help="Amazon only"),
    vendor_id: str | None = typer.Option(None, help="ClickBank vendor"),
) -> None:
    """Import from human research (Digistore24, ClickBank, Amazon). Payout via Nomad."""
    repo = OpportunityRepository()
    opp_id = import_affiliate_manual(
        repo,
        platform=platform,
        keyword=keyword,
        product_name=product_name,
        price=price,
        affiliate_url=affiliate_url,
        commission_pct=commission_pct,
        cookie_days=cookie_days,
        refund_rate=refund_rate,
        gravity=gravity,
        rating=rating,
        reviews=reviews,
        vendor_id=vendor_id,
    )
    typer.echo(f"Imported {platform} opportunity: {opp_id}")


@app.command("filter")
def filter_cmd(vertical: str = typer.Option("physical")) -> None:
    repo = OpportunityRepository()
    rules = load_physical_rules()
    pending = repo.list_by_status("PENDING", vertical=vertical)
    rejected = 0
    for opp in pending:
        ok, reason = apply_physical_filters(opp, rules)
        if ok:
            continue
        opp.status = "REJECTED"
        opp.reject_reason = reason
        repo.upsert(opp)
        rejected += 1
    typer.echo(f"Filtered: {rejected} rejected of {len(pending)} pending")


@app.command("score")
def score_cmd(vertical: str = typer.Option("physical")) -> None:
    repo = OpportunityRepository()
    rules = load_physical_rules()
    rows = repo.list_by_status("PENDING", vertical=vertical)
    validated = 0
    for opp in rows:
        scored = score_physical(opp, rules)
        repo.upsert(scored)
        if scored.status == "VALIDATED":
            validated += 1
    typer.echo(f"Scored: {validated} VALIDATED of {len(rows)} pending")


@app.command("rank")
def rank(
    vertical: str = typer.Option("physical"),
    limit: int = typer.Option(3),
) -> None:
    repo = OpportunityRepository()
    items = repo.list_by_status("VALIDATED", vertical=vertical)[:limit]
    for i, opp in enumerate(items, 1):
        typer.echo(
            f"{i}. {opp.product_name or opp.keyword} | "
            f"EPC=${opp.estimated_epc} matrix={opp.matrix_score} "
            f"id={opp.id}"
        )


@app.command("list")
def list_cmd(status: str = typer.Option("VALIDATED")) -> None:
    repo = OpportunityRepository()
    for opp in repo.list_by_status(status, vertical="physical"):
        typer.echo(f"{opp.id} | {opp.status} | {opp.keyword[:60]}")


@app.command("export")
def export(
    id: str = typer.Option(..., "--id"),
    output: Path = typer.Option(Path("storage/exports")),
) -> None:
    repo = OpportunityRepository()
    data = repo.export_json(id)
    output.mkdir(parents=True, exist_ok=True)
    path = output / f"{id}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    typer.echo(f"Exported {path}")


@app.command("weekly-cycle")
def weekly_cycle(
    output: Path = typer.Option(Path("storage/exports")),
) -> None:
    """Physical MVP pipeline: ingest → filter → score → rank top 3 → export."""
    repo = OpportunityRepository()
    total = ingest_reddit_physical(repo)
    typer.echo(f"Ingested {total} opportunities")

    rules = load_physical_rules()
    pending = repo.list_by_status("PENDING", vertical="physical")
    rejected = 0
    for opp in pending:
        ok, reason = apply_physical_filters(opp, rules)
        if ok:
            continue
        opp.status = "REJECTED"
        opp.reject_reason = reason
        repo.upsert(opp)
        rejected += 1
    typer.echo(f"Filtered: {rejected} rejected")

    pending = repo.list_by_status("PENDING", vertical="physical")
    validated = 0
    for opp in pending:
        scored = score_physical(opp, rules)
        repo.upsert(scored)
        if scored.status == "VALIDATED":
            validated += 1
    typer.echo(f"Scored: {validated} VALIDATED")

    items = repo.list_by_status("VALIDATED", vertical="physical")[:3]
    for i, opp in enumerate(items, 1):
        typer.echo(
            f"{i}. {opp.product_name or opp.keyword} | EPC=${opp.estimated_epc} id={opp.id}"
        )
    output.mkdir(parents=True, exist_ok=True)
    for opp in items:
        data = repo.export_json(opp.id)
        path = output / f"{opp.id}.json"
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        typer.echo(f"Exported {path}")


if __name__ == "__main__":
    app()
