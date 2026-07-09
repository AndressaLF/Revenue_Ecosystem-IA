# RE-IA — Revenue Ecosystem IA

Laboratório modular para afiliados USD: **Digistore24**, **ClickBank**, **Amazon** (físico). Recebimento via **Nomad**.

## Contas ativas

| Plataforma | Uso |
|------------|-----|
| Digistore24 | Marketplace digital — cookie 180d |
| ClickBank | Marketplace digital — gravity ≥ 20 |
| Nomad | Recebimento USD |
| Amazon | Físicos (quando Associates aprovado) |

Guia humano: [docs/17-human-affiliate-sources.md](docs/17-human-affiliate-sources.md)

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edite .env — mínimo: GEMINI_API_KEY (ver docs/18-secrets-and-env.md)
python -m shared_components.config.check_env
python -m shared_components.database.init_db
```

### Importar produto (pesquisa humana no marketplace)

```bash
# ClickBank
python -m modules.opportunity_finder.cli import-affiliate \
  --platform clickbank \
  --keyword "program honest review" \
  --product-name "Product Name" \
  --price 47 \
  --affiliate-url "https://hop.clickbank.net/?affiliate=YOU&vendor=VENDOR" \
  --commission-pct 50 \
  --gravity 35

# Digistore24
python -m modules.opportunity_finder.cli import-affiliate \
  --platform digistore24 \
  --keyword "product worth it review" \
  --product-name "Product Name" \
  --price 97 \
  --affiliate-url "https://www.digistore24.com/redir/YOUR_LINK" \
  --commission-pct 25

# Amazon (físico)
python -m modules.opportunity_finder.cli import-affiliate \
  --platform amazon \
  --keyword "best cable tray for desk" \
  --product-name "Cable Tray" \
  --price 42.99 \
  --affiliate-url "https://www.amazon.com/dp/ASIN?tag=TAG" \
  --rating 4.5 --reviews 200
```

### Pipeline

```bash
python -m modules.opportunity_finder.cli ingest --source reddit
python -m modules.opportunity_finder.cli filter
python -m modules.opportunity_finder.cli score
python -m modules.opportunity_finder.cli rank --limit 3
python -m modules.physical_affiliate.cli produce --id <ID>
```

Publicar: Medium (EN) + FTC — nunca hoplink bruto em Pinterest/Reddit.

## GitHub Pages (Reddit API)

Página pública do projeto: [docs/index.html](docs/index.html) — necessária para cadastrar o app Reddit.

Passo a passo: [docs/GITHUB_PAGES.md](docs/GITHUB_PAGES.md)
