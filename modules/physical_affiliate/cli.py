from __future__ import annotations

import json
import os
import re
from pathlib import Path

import typer
from jinja2 import Template

from shared_components.compliance.ftc_disclosure import FTC_HTML, FTC_MARKDOWN
from shared_components.database.schema import init_db
from shared_components.database.sqlite_repo import OpportunityRepository

app = typer.Typer(help="RE-IA physical affiliate production")

REVIEW_MD = """
# {{ title }}

{{ ftc_md }}

## The problem

{{ pain_statement or "Many home office workers struggle with desk clutter and cable mess." }}

## Who this is for

**Persona:** {{ persona_tag or "home_consumer" }} — US buyers looking for practical upgrades in the ${{ price_min }}–${{ price_max }} range.

## What we looked at

We evaluated **{{ product_name }}** for {{ keyword_context }}.

### Pros
- Solves a specific physical pain point (not just aesthetics)
- Strong social proof on Amazon (check latest reviews before buying)
- Fits impulse-buy pricing for home office upgrades

### Cons
- Amazon cookie is 24 hours — decide when you're ready to buy
- {{ con_2 }}
- {{ con_3 }}

## Verdict

If {{ pain_short }}, this is worth testing. Use the link below after reading current reviews and checking stock.

**[Check price and availability on Amazon]({{ affiliate_url }})**

---
*Last updated: {{ updated }}*
""".strip()

REVIEW_HTML = """
<article>
  <h1>{{ title }}</h1>
  {{ ftc_html|safe }}
  <h2>The problem</h2>
  <p>{{ pain_statement }}</p>
  <h2>Who this is for</h2>
  <p><strong>Persona:</strong> {{ persona_tag }} — practical US home office buyers.</p>
  <h2>Review: {{ product_name }}</h2>
  <h3>Pros</h3>
  <ul>
    <li>Targets a real desk/home pain point</li>
    <li>Price zone fits impulse purchases</li>
    <li>Easy to compare on Amazon</li>
  </ul>
  <h3>Cons</h3>
  <ul>
    <li>24-hour affiliate cookie on Amazon</li>
    <li>{{ con_2 }}</li>
    <li>{{ con_3 }}</li>
  </ul>
  <p><a href="{{ affiliate_url }}" rel="nofollow sponsored">Check price on Amazon</a></p>
</article>
""".strip()


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:80]


def build_affiliate_url(base_url: str, opportunity_id: str, channel: str = "medium") -> str:
    tag = os.getenv("AMAZON_ASSOCIATE_TAG", "")
    sep = "&" if "?" in base_url else "?"
    url = f"{base_url}{sep}ref={channel}_{opportunity_id}"
    if tag and "tag=" not in url:
        url += f"&tag={tag}"
    return url


@app.callback()
def _init() -> None:
    init_db()


@app.command("produce")
def produce(
    id: str = typer.Option(..., "--id"),
    output: Path = typer.Option(Path("modules/physical_affiliate/output")),
) -> None:
    repo = OpportunityRepository()
    opp = repo.get(id)
    if not opp:
        raise typer.BadParameter(f"Unknown opportunity: {id}")
    if not opp.affiliate_url:
        raise typer.BadParameter("affiliate_url required — import-amazon with full URL first")

    affiliate_url = build_affiliate_url(opp.affiliate_url, opp.id)
    title = f"Best {opp.product_name or opp.keyword} for Small Desks (Honest Review)"
    ctx = {
        "title": title,
        "ftc_md": FTC_MARKDOWN,
        "ftc_html": FTC_HTML,
        "pain_statement": opp.pain_statement or opp.keyword,
        "persona_tag": opp.persona_tag,
        "price_min": 35,
        "price_max": 75,
        "product_name": opp.product_name or "this product",
        "keyword_context": opp.keyword,
        "pain_short": "your desk cables are a daily frustration",
        "con_2": "May be out of stock during peak season — verify before promoting",
        "con_3": "Not a substitute for ergonomic assessment if you have chronic pain",
        "affiliate_url": affiliate_url,
        "updated": "2026-07",
    }

    output.mkdir(parents=True, exist_ok=True)
    slug = slugify(title)
    md_path = output / f"{slug}.md"
    html_path = output / f"{slug}.html"
    meta_path = output / f"{slug}.meta.json"

    md_path.write_text(Template(REVIEW_MD).render(**ctx), encoding="utf-8")
    html_path.write_text(Template(REVIEW_HTML).render(**ctx), encoding="utf-8")
    meta = {
        "opportunity_id": opp.id,
        "vertical": "physical",
        "channel_primary": "pinterest",
        "channel_bridge": "medium",
        "affiliate_url": affiliate_url,
        "checklist": [
            "Publish article on Medium (EN)",
            "Create 10 Pinterest pins 2:3 → link to Medium only",
            "Never post raw Amazon link on Reddit",
            "Register views/clicks in metrics spreadsheet",
        ],
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    opp.status = "PRODUCED"
    repo.upsert(opp)
    typer.echo(f"Produced:\n  {md_path}\n  {html_path}\n  {meta_path}")


if __name__ == "__main__":
    app()
