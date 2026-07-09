# 🔌 APIs e Fontes de Dados Gratuitas

> Catálogo priorizado para **mercado internacional (USD / inglês)**: API oficial > RSS/JSON > scraping resiliente.

**Referências:** [Audience Intelligence](./15-audience-intelligence.md) · [Enriquecimento de campos](#-matriz-de-enriquecimento-campo--ferramenta--método) · [Automação](./14-deploy.md)

---

## 📑 Sumário

1. [Ordem de Preferência](#-ordem-de-preferência)
2. [Ferramentas Gratuitas — Mercado Internacional](#-ferramentas-gratuitas--mercado-internacional)
3. [Fontes Humanas — Marketplaces Afiliados](#-fontes-humanas--marketplaces-afiliados)
4. [Matriz de Enriquecimento: Campo → Ferramenta → Método](#-matriz-de-enriquecimento-campo--ferramenta--método)
4. [Fontes por Pilar](#-fontes-por-pilar)
5. [Conectores MVP (Fase 1)](#-conectores-mvp-fase-1)
6. [Fontes por Vertical](#-fontes-por-vertical)
7. [Regras de Implementação](#-regras-de-implementação)

---

## 📶 Ordem de Preferência

```
1. API oficial gratuita
2. RSS / Atom / JSON público
3. Sitemap / CSV público
4. Scraping leve com rate-limit e cache
5. ❌ Scraping pesado / APIs pagas (proibido no MVP)
```

**Locale padrão:** `en-US`, `geo=US` (ajustável para UK/CA/AU no futuro).

---

## 🌍 Ferramentas Gratuitas — Mercado Internacional

Stack **gratuita e inteligente** para pesquisa, validação e enriquecimento em mercados USD — sem Ahrefs/Semrush no MVP.

### Pesquisa de demanda e tendência

| Ferramenta | Tipo | Custo | Dados USD | Uso no RE-IA |
|------------|------|-------|-----------|--------------|
| **Google Trends** (`pytrends`) | Não-oficial | Grátis | US/UK/CA | `search_volume` relativo, `trend_velocity` |
| **Google Autosuggest** | HTTP GET | Grátis | EN queries | Cauda longa transacional, confirma persona |
| **Reddit** (`.json` / API) | API/OAuth | Grátis | Comunidades EN | `pain_signals`, `persona_tag`, urgência |
| **Product Hunt** | API GraphQL | Grátis | Global SaaS | Lançamentos, comentários = dor B2B |
| **Hacker News** | Firebase API | Grátis | Tech EN | `developer` persona, `tool_friction` |
| **GitHub Trending** | RSS/scrape leve | Grátis | Dev global | Sinais `developer` + `saas` |
| **Indie Hackers** | RSS | Grátis | Indie SaaS | Dor de monetização, pricing |
| **Pinterest Trends** | Export manual | Grátis | US visual | `creator`, `home_consumer`, templates |
| **Exploding Topics** *(manual)* | Web | Freemium limitado | US trends | Validação humana trimestral |

### Validação e inteligência local (sem nuvem)

| Ferramenta | Tipo | Custo | Uso no RE-IA |
|------------|------|-------|--------------|
| **DuckDB** | OLAP local | Grátis | Agregação `pain_by_persona`, concorrência |
| **sentence-transformers** | Embeddings CPU | Grátis | Cluster dor, cache semântico |
| **SQLite** | OLTP local | Grátis | Estado, cache HTTP 24h |
| **feedparser** | RSS | Grátis | Notícias nicho EN |

### Produção e compliance (pós-validação)

| Ferramenta | Tipo | Custo | Uso |
|------------|------|-------|-----|
| **Gemini API** | LLM | Pay-per-use mínimo | Score top N, JTBD opcional |
| **Medium** | Publicação | Grátis | Ponte afiliado — canal EN |
| **Pinterest** | Publicação | Grátis | Topo funil visual |
| **YouTube** | Publicação | Grátis | Tutorial SaaS EN |

### O que NÃO usar no MVP

| Ferramenta | Motivo |
|------------|--------|
| Ahrefs, Semrush, Moz | Pago |
| Jungle Scout (API) | Pago — BS/M&S manual OK para físicos |
| Scraping Amazon em escala | ToS + ban IP |
| Twitter/X API | Custo / instabilidade |
| Ferramentas de "caça trending AI" | Distração ([00-vision](./00-vision.md)) |

---

## 🤝 Fontes Humanas — Marketplaces Afiliados

> **Sem API no MVP** — pesquisa no painel + `import-affiliate` CLI.  
> Contas ativas: **Digistore24**, **ClickBank**, **Nomad** (USD). Guia: [17-human-affiliate-sources](./17-human-affiliate-sources.md)

| Plataforma | URL pesquisa | Vertical | Campos humanos → schema |
|------------|--------------|----------|-------------------------|
| **Digistore24** | Marketplace affiliate | `digital` | hoplink, preço, comissão %, refund |
| **ClickBank** | Marketplace + Affiliate Tools | `digital` | hoplink, gravity, avg $/sale, vendor |
| **Amazon** | BS / Movers & Shakers | `physical` | ASIN link, preço, rating, reviews |
| **Nomad** | App Nomad | payout | reconciliação USD (não é fonte de produto) |

### Enriquecimento via painel (humano)

| Campo | Digistore24 | ClickBank | Amazon |
|-------|-------------|-----------|--------|
| `affiliate_url` | Hoplink | Hoplink | Link + tag |
| `commission_pct` | Painel produto | Affiliate tools | 1–3% categoria |
| `cookie_days` | 180 | 60 | 24 |
| `estimated_price` | Preço venda | Avg sale | Preço listing |
| `refund_rate` | Stats | Marketplace | N/A |
| `estimated_epc` | Calculado no import | gravity + EPC painel | Calculado no import |

Config: `config/human_sources.yaml` · `config/affiliate_programs.yaml`

---

## 📊 Matriz de Enriquecimento: Campo → Ferramenta → Método

Como popular cada campo do schema `opportunities` e `pain_signals` — referência para `audience/enricher.py`.

### Campos de identidade e mercado

| Campo schema | Ferramenta | Método | Frequência | Automático? |
|--------------|------------|--------|------------|-------------|
| `keyword` | Autosuggest + Reddit | Merge queries transacionais EN | 3×/semana | ✅ |
| `source` | Conector ingest | Tag do conector (`reddit`, `trends`…) | 3×/semana | ✅ |
| `vertical` | `channel_matcher.py` | Regra persona+pain → vertical | pós-classify | ✅ |
| `product_name` | Product Hunt / manual | Nome do launch ou inferido da keyword | ingest | ✅/⚠️ |
| `affiliate_url` | Painel afiliado | Humano cola após aprovar top 3 | sob demanda | ❌ |
| `raw_data` | Todos conectores | JSON minificado da resposta HTTP | ingest | ✅ |

### Campos Audience Intelligence

| Campo schema | Ferramenta | Método | Frequência | Automático? |
|--------------|------------|--------|------------|-------------|
| `persona_tag` | Reddit + `persona_rules.yaml` | Match subreddit + keywords | 3×/semana | ✅ |
| `persona_confidence` | Regras + embeddings | Score 0–1 por matches | 3×/semana | ✅ |
| `pain_statement` | Reddit/PH + cluster | Maior engagement no cluster | 3×/semana | ✅ |
| `pain_category` | `pain_patterns.yaml` | Regex EN | 3×/semana | ✅ |
| `pain_urgency_score` | Reddit engagement | `≥30` → +0.25 + heurísticas | 3×/semana | ✅ |
| `jtbd_statement` | `jtbd_templates.py` / Gemini | Template; LLM 1/cluster se necessário | 3×/semana | ✅/⚠️ |
| `suggested_channel` | `channel_matcher.py` | vertical + cookie + persona | pós-match | ✅ |

### Campos `pain_signals` (tabela auxiliar)

| Campo | Ferramenta | Método |
|-------|------------|--------|
| `raw_text` | Reddit `.json` | Título + top comments |
| `engagement_score` | Reddit API | upvotes + num_comments |
| `persona_hint` | subreddit map | Pré-classificação |
| `pain_category` | regex | Mesmos padrões do estágio EXTRACT_PAIN |
| `opportunity_id` | merge step | FK após cluster |

### Campos de métricas e economia

| Campo schema | Ferramenta | Método | Frequência |
|--------------|------------|--------|------------|
| `search_volume` | Google Trends (`pytrends`) | Interesse relativo 0–100; normalizar | 3×/semana |
| `competition_score` | DuckDB + heurística | Densidade keywords similares / proxy KD | 3×/semana |
| `trend_velocity` | Trends (slope 90d) | Δ interesse / tempo | 3×/semana |
| `intent_score` | Regex + Autosuggest | Modificadores transacionais | 3×/semana |
| `estimated_price` | Gumroad/Etsy discover / PH | Scrape leve ou manual | ingest |
| `commission_pct` | Site programa afiliado | Humano ou tabela estática YAML | trimestral |
| `cookie_days` | Tabela afiliados YAML | `config/affiliate_programs.yaml` | trimestral |
| `estimated_epc` | Cálculo local | `conv_est × price × commission` | pós-score |
| `fci_score` | Fórmula | [micro_assets](./smart/micro_assets.md) | pós-enrich |
| `iema_score` | Fórmula | [saas_microsaas](./smart/saas_microsaas.md) | pós-enrich |
| `churn_monthly` | Playbook / PH comments | Default vertical ou manual | ingest |
| `arpu_monthly` | Site pricing / PH | Scrape pricing page | ingest |
| `lp_quality_score` | Humano | Checklist 1–5 ao testar produto | pré-PRODUCED |
| `friction_score` | Heurística produto | clone 1-click=1, zip=5 | ingest |

### Campos de controle

| Campo | Ferramenta | Método |
|-------|------------|--------|
| `opportunity_score` | `vertical_scoring.py` | Peso composto + frameworks |
| `ai_score` | Gemini (top N) | Structured output Pydantic |
| `status` | pipeline | PENDING → REJECTED/VALIDATED |
| `reject_reason` | heuristics H-10…H-14 | Código da regra |
| `enrichment_source` | enricher | JSON: `{field: source}` |
| `last_enriched_at` | enricher | timestamp UTC |

### Pipeline de enriquecimento (ordem)

```
1. INGEST preenche: keyword, source, raw_data, product_name (se houver)
2. EXTRACT_PAIN preenche: pain_signals.*
3. CLASSIFY_PERSONA preenche: persona_tag, persona_confidence
4. ENRICH preenche: search_volume, trend_velocity, pain_statement, jtbd_statement
5. MATCH preenche: vertical, suggested_channel
6. SCORE preenche: intent_score, fci/iema/epc, opportunity_score, ai_score
7. Humano preenche: affiliate_url, lp_quality_score (após teste)
```

---

## 🗂️ Fontes por Pilar

### Pilar 1 — Pesquisa (EN / USD)

| Fonte | Método | Dados | Módulo |
|-------|--------|-------|--------|
| Google Trends | `pytrends` (`hl=en-US`, `geo=US`) | Volume relativo, tendência | 01 |
| Reddit | API / `.json` | Dores, persona, engagement | 01 |
| Product Hunt | API gratuita | Lançamentos SaaS | 01, 02 |
| Hacker News | Firebase API | Tech trends | 01 |
| GitHub Trending | RSS/scrape leve | Repos em alta | 01 |
| Google Autosuggest | HTTP (`hl=en`, `gl=us`) | Cauda longa | 01, 03 |
| Pinterest Trends | Export manual | Nichos visuais | 01, 03 |
| Etsy / Gumroad discover | Autosuggest + scrape leve | Digital intent | 01, 03 |
| RSS feeds (EN) | `feedparser` | Notícias nicho | 01 |
| Indie Hackers | RSS | SaaS indie pain | 01 |

### Pilar 1.5 — Audience Intelligence

| Fonte | Campos enriquecidos |
|-------|---------------------|
| Reddit comments | `pain_*`, `persona_*`, `pain_urgency_score` |
| Embeddings locais | cluster, `jtbd_statement` |
| `persona_rules.yaml` | `persona_tag`, `persona_confidence` |

### Pilar 2 — Validação

| Fonte | Uso |
|-------|-----|
| DuckDB agregações | Concorrência, `pain_by_persona` |
| `heuristics.py` | H-01…H-14 |
| Gemini (último recurso) | `ai_score` top N |

---

## 🚀 Conectores MVP (Fase 1)

| # | Conector | Arquivo | Prioridade | Locale |
|---|----------|---------|------------|--------|
| 1 | Google Trends | `ingest/trends.py` | P0 | en-US, US |
| 2 | Reddit scout | `ingest/reddit.py` | P0 | subreddits EN |
| 3 | Autosuggest | `ingest/autosuggest.py` | P0 | hl=en, gl=us |
| 4 | Product Hunt | `ingest/producthunt.py` | P1 | global |
| 5 | RSS genérico | `ingest/rss.py` | P1 | EN feeds |
| 6 | Hacker News | `ingest/hackernews.py` | P1 | — |
| 7 | Pinterest Trends | `ingest/pinterest.py` | P2 | manual export |
| 8 | Gumroad/Etsy discover | `ingest/marketplaces.py` | P2 | scrape leve |

---

## 🏷️ Fontes por Vertical (mercado EN)

| Vertical | Fontes | Padrões keyword EN | Playbook |
|----------|--------|-------------------|----------|
| SaaS | PH, Reddit r/SaaS, HN | `[name] vs`, `alternatives`, `review` | [saas_microsaas](./smart/saas_microsaas.md) |
| Templates | Autosuggest, Etsy, Pinterest, r/Notion | `template for [job]`, `notion CRM` | [micro_assets](./smart/micro_assets.md) |
| Físicos | Amazon BS/M&S *(manual)*, Trends | `best [product] for [context]` | [physical_products](./smart/physical_products.md) |
| Digitais (DS24/CB) | Marketplace *(manual)*, Reddit dor | `{product} review`, `worth it` | [17-human-affiliate](./17-human-affiliate-sources.md) |

---

## 📐 Regras de Implementação

| Regra | Detalhe |
|-------|---------|
| Locale | `en-US` default; filtrar conteúdo não-EN no MVP |
| Rate limit | Máx. 1 req/s por domínio; cache 24h SQLite |
| User-Agent | Identificar bot + contact no README |
| Retry | 3× backoff exponencial |
| ToS | robots.txt; exceções em [12-risks](./12-risks.md) |
| Auth | Keys gratuitas em `.env` apenas |
| Enriquecimento | Log `enrichment_source` por campo |
| Testes | Mock HTTP em pytest |

### Variáveis de ambiente

```env
GEMINI_API_KEY=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
PRODUCTHUNT_TOKEN=
INGEST_LOCALE=en-US
INGEST_GEO=US
LOG_LEVEL=INFO
```

### Config estática (sem API)

```yaml
# config/affiliate_programs.yaml
programs:
  - name: nomad
    cookie_days: 90
    commission_pct: 30
    vertical: saas
```

---

*Última atualização: julho/2026*
