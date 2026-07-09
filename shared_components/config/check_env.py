"""Print which environment variables are configured (no secret values)."""

from __future__ import annotations

from shared_components.config.settings import get_settings


def main() -> None:
    s = get_settings()
    checks = [
        ("GEMINI_API_KEY", s.gemini_configured(), "P0 — IA produce / auto-select"),
        ("REDDIT OAuth", s.reddit_oauth_configured(), "P2 — rate limit Reddit"),
        ("CLICKBANK_NICKNAME", bool(s.clickbank_nickname), "P1 — hoplinks"),
        ("DIGISTORE24_AFFILIATE_ID", bool(s.digistore24_affiliate_id), "P1 — hoplinks"),
        ("AMAZON_ASSOCIATE_TAG", bool(s.amazon_associate_tag), "P1 — físico"),
        ("DIGISTORE24_API_KEY", s.digistore24_api_key is not None, "P2 — scout API"),
        ("CLICKBANK_API_KEY", s.clickbank_api_key is not None, "P2 — Analytics API (metricas)"),
        ("MEDIUM_INTEGRATION_TOKEN", s.medium_integration_token is not None, "P3 — publish"),
        ("PINTEREST_ACCESS_TOKEN", s.pinterest_access_token is not None, "P3 — pins API"),
        ("PRODUCTHUNT_TOKEN", s.producthunt_token is not None, "P3 — SaaS ingest"),
    ]
    print("RE-IA environment check\n")
    for name, ok, note in checks:
        status = "OK" if ok else "—"
        print(f"  [{status:2}] {name:<28} {note}")
    print("\nArquivo: .env (nao commitar)")
    if not s.gemini_configured():
        print("\nAVISO: GEMINI_API_KEY ausente — produce com IA nao funcionara.")


if __name__ == "__main__":
    main()
