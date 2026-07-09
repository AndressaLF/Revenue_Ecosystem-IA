# 🗄️ Banco de Dados

> SQLite (operacional) + DuckDB (analítico) — zero custo de nuvem.

**Referências:** [Arquitetura](./02-architecture.md) · [Módulos](./03-modules.md)

---

## 📑 Sumário

1. [Visão Geral](#-visão-geral)
2. [SQLite — Tabelas](#-sqlite--tabelas)
3. [Campos dos Playbooks](#campos-derivados-dos-playbooks)
4. [DuckDB — Análises](#-duckdb--análises)
5. [Cache e IA](#-cache-e-ia)
6. [Convenções](#-convenções)

---

## 🎯 Visão Geral

| Banco | Arquivo | Responsável |
|-------|---------|-------------|
| SQLite | `storage/local_cache.db` | Estado, cache, oportunidades |
| DuckDB | `storage/analytics.duckdb` | Agregações OLAP de ingestão |

---

## 📋 SQLite — Tabelas

### `opportunities`

```sql
CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    keyword TEXT NOT NULL,
    vertical TEXT NOT NULL,           -- 'saas' | 'template' | 'digital' | 'physical'
    product_name TEXT,
    affiliate_url TEXT,
    raw_data TEXT,
    -- Métricas de mercado (playbooks smart/)
    search_volume INTEGER DEFAULT 0,
    competition_score REAL DEFAULT 0.0,  -- KD proxy 0-100
    trend_velocity REAL DEFAULT 0.0,
    intent_score REAL DEFAULT 0.0,       -- 0-1 transacional vs informativo
    -- Audience Intelligence (15-audience-intelligence)
    persona_tag TEXT,                    -- freelancer, developer, home_consumer, ...
    persona_confidence REAL DEFAULT 0.0, -- 0-1 confiança da classificação
    persona_signals TEXT,                -- JSON: sinais que levaram à tag
    pain_statement TEXT,                 -- dor em linguagem real (EN)
    pain_category TEXT,                  -- time_waste, organization, tool_friction, ...
    pain_urgency_score REAL DEFAULT 0.0, -- boost Reddit 30+ comentários
    jtbd_statement TEXT,                 -- Job-to-be-Done acionável
    suggested_channel TEXT,              -- pinterest, medium, youtube, ...
    -- Economia (EPC, FCI, IEMA)
    estimated_price REAL DEFAULT 0.0,
    commission_pct REAL DEFAULT 0.0,
    cookie_days INTEGER DEFAULT 0,
    estimated_epc REAL DEFAULT 0.0,
    fci_score REAL,                      -- micro_assets
    iema_score REAL,                     -- saas_microsaas
    matrix_score REAL DEFAULT 0.0,       -- matriz 0-100 ponderada
    friction_score INTEGER DEFAULT 3,    -- 1=clone 1-click, 5=zip pesado
    lp_quality_score INTEGER DEFAULT 3,  -- 1-5 nota LP (FCI)
    churn_monthly REAL,                  -- saas only
    arpu_monthly REAL,                   -- saas only
    refund_rate REAL,                    -- physical only
    -- Scores finais
    opportunity_score REAL DEFAULT 0.0,
    ai_score REAL DEFAULT 0.0,
    status TEXT DEFAULT 'PENDING',
    reject_reason TEXT,
    enrichment_source TEXT,              -- JSON: {campo: fonte} — ver 06-apis
    last_enriched_at TIMESTAMP,
    produced_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Campos derivados dos playbooks

| Campo | Playbook | Uso |
|-------|----------|-----|
| `fci_score` | [micro_assets](./smart/micro_assets.md) | `rank --vertical template` |
| `iema_score` | [saas_microsaas](./smart/saas_microsaas.md) | `rank --vertical saas` |
| `estimated_epc` | todos | Desempate e dashboard ROI |
| `intent_score` | todos | Penalizar "tips", "how to" genérico |
| `cookie_days` | saas/digital | Hard-fail se abaixo do mínimo |
| `persona_tag` | [15-audience](./15-audience-intelligence.md) | Agregação e match canal |
| `persona_confidence` | [15-audience](./15-audience-intelligence.md) | Gate H-14; manual_review se < 0.5 |
| `pain_statement` | [15-audience](./15-audience-intelligence.md) | Copy de produção (02/03) |
| `jtbd_statement` | [15-audience](./15-audience-intelligence.md) | Estrutura review/funnel |
| `suggested_channel` | [15-audience](./15-audience-intelligence.md) | Checklist de publicação |
| `enrichment_source` | [06-apis](./06-apis.md) | Rastreabilidade campo → ferramenta |
| `last_enriched_at` | enricher | Auditoria do pipeline |

### `pain_signals`

Sinais brutos extraídos antes de agregar em `opportunities`:

```sql
CREATE TABLE IF NOT EXISTS pain_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,              -- 'reddit', 'producthunt', ...
    source_url TEXT,
    raw_text TEXT NOT NULL,
    pain_category TEXT,
    persona_hint TEXT,
    engagement_score INTEGER DEFAULT 0,  -- upvotes, comments
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    opportunity_id TEXT,               -- FK após match
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
);
```

### `metrics`

```sql
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id TEXT NOT NULL,
    channel TEXT NOT NULL,            -- 'medium', 'pinterest', 'reddit'
    views INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    revenue_usd REAL DEFAULT 0.0,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
);
```

### `ai_cache`

```sql
CREATE TABLE IF NOT EXISTS ai_cache (
    cache_key TEXT PRIMARY KEY,       -- MD5 ou hash semântico
    cache_type TEXT NOT NULL,         -- 'hash' | 'semantic'
    prompt_hash TEXT NOT NULL,
    response_json TEXT NOT NULL,
    embedding BLOB,                   -- opcional para semântico
    tokens_saved INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);
```

### Ciclo de status

| Status | Próximo passo |
|--------|---------------|
| `PENDING` | `filter` |
| `REJECTED` | Arquivo morto — não produzir |
| `VALIDATED` | `02` ou `03 produce` |
| `PRODUCED` | Publicar + `metrics` |

---

## 📊 DuckDB — Análises

Criadas em runtime pelo `analytics_engine`:

| View/Tabela | Uso |
|-------------|-----|
| `raw_ingest` | Dados brutos por fonte e timestamp |
| `keyword_stats` | volume médio, desvio, tendência |
| `competitor_density` | contagem por keyword/nicho |
| `vertical_rank` | ranking para decisão humana |
| `pain_by_persona` | volume de dor agregado por persona/categoria |

---

## 💾 Cache e IA

- **Hash cache:** `ai_cache` com `cache_type='hash'`, TTL 7 dias
- **Semântico:** embedding em BLOB + busca cosseno antes de insert
- Métrica `tokens_saved` alimenta [13-metrics](./13-metrics.md)

---

## 📐 Convenções

| Regra | Detalhe |
|-------|---------|
| IDs | `sha256(f"{keyword}:{source}")[:16]` |
| `raw_data` | JSON minificado — nunca enviar integral à IA |
| Migrations | `shared_components/database/migrations/` |
| Git | `storage/` sempre no `.gitignore` |

---

*Última atualização: julho/2026*
