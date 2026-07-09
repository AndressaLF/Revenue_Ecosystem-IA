# 🔄 Fluxos Operacionais

> Diagramas e sequências para implementação pelo Cursor.

**Referências:** [Arquitetura](./02-architecture.md) · [Módulos](./03-modules.md)

---

## 📑 Sumário

1. [Fluxo Macro do Ecossistema](#-fluxo-macro-do-ecossistema)
2. [Fluxo Audience Intelligence](#-fluxo-audience-intelligence)
3. [Fluxo de Pesquisa e Validação](#-fluxo-de-pesquisa-e-validação)
3. [Fluxo de Produção SaaS](#-fluxo-de-produção-saas)
4. [Fluxo de Decisão (Pivot)](#-fluxo-de-decisão-pivot)
5. [Fluxo de Chamada IA](#-fluxo-de-chamada-ia)

---

## 🌐 Fluxo Macro do Ecossistema

```mermaid
flowchart LR
    subgraph FONTES["Fontes Gratuitas"]
        RSS[RSS]
        REDDIT[Reddit]
        TRENDS[Google Trends]
        PH[Product Hunt]
    end

    subgraph CORE["shared_components"]
        CACHE[cache]
        DB[(SQLite + DuckDB)]
        IA[gemini_client]
    end

    subgraph P12["01_opportunity_finder"]
        INGEST[ingest]
        AUDIENCE[extract-pain + persona]
        FILTER[filter]
        SCORE[score]
    end

    subgraph PROD["Produção"]
        M02[02_affiliate_saas]
        M03[03_notion_funnel]
    end

    subgraph OUT["Saída"]
        MD[Markdown/HTML]
        PUB[Publicação]
        DASH[Dashboard]
    end

    FONTES --> INGEST
    INGEST --> AUDIENCE
    AUDIENCE --> DB
    AUDIENCE --> FILTER
    FILTER --> SCORE
    SCORE --> CACHE
    CACHE --> IA
    SCORE --> DB
    DB --> M02
    DB --> M03
    M02 --> MD
    M03 --> MD
    MD --> PUB
    PUB --> DASH
```

---

## 🎯 Fluxo Audience Intelligence

> Camada entre ingest e validação — [15-audience-intelligence](./15-audience-intelligence.md)

```mermaid
flowchart TD
    ING[ingest Reddit/PH/Trends] --> EXT[extract-pain]
    EXT --> PS[(pain_signals)]
    EXT --> CLS[classify-persona + JTBD]
    CLS --> OPP[(opportunities + persona_tag)]
    CLS --> MATCH[match vertical + canal]
    MATCH --> FIL[filter hard-fail]
    FIL --> SCR[score FCI/IEMA/EPC]
    SCR --> RNK[rank top 3]
    RNK --> EXP[export JSON → 02/03]
    EXP --> HUM{Humano aprova 1}
    HUM -->|Sim| PROD[produce]
    HUM -->|Não| RNK
```

### Ciclo 3× por semana (`weekly-cycle`)

| Dia | Ação |
|-----|------|
| Segunda 08:00 | `weekly-cycle` → top 3 |
| Quarta 08:00 | `weekly-cycle` → top 3 |
| Sexta 08:00 | `weekly-cycle` + relatório persona/EPC |

---

## 🔍 Fluxo de Pesquisa e Validação

```mermaid
sequenceDiagram
    participant CLI as 01 CLI
    participant API as Fontes Grátis
    participant DUCK as DuckDB
    participant FILT as Filtro Local
    participant CACHE as semantic_cache
    participant GEM as Gemini Pro
    participant SQL as SQLite

    CLI->>API: ingest()
    API->>DUCK: raw aggregates
    API->>SQL: opportunities PENDING

    CLI->>FILT: extract-pain + classify-persona
    FILT->>SQL: pain_signals + persona_tag

    CLI->>FILT: filter()
    FILT->>SQL: REJECTED (~90%)

    CLI->>FILT: score(use_ai=true)
    FILT->>CACHE: check similarity
    alt cache hit
        CACHE-->>CLI: cached JSON score
    else cache miss
        CACHE->>GEM: compressed prompt
        GEM-->>CACHE: structured score
        CACHE->>SQL: VALIDATED + ai_score
    end
```

### Hard-fail filters (sem IA)

| Regra | Ação |
|-------|------|
| `search_volume < 1000` | REJECTED |
| `competition_score > 50` | REJECTED |
| Duplicata (mesmo keyword+source) | SKIP |
| Fonte indisponível | LOG + retry manual |

---

## 💼 Fluxo de Produção SaaS

```mermaid
flowchart TD
    A[list VALIDATED] --> B{Escolher oportunidade}
    B --> C[02 produce --id]
    C --> D[Carregar oportunidade SQLite]
    D --> E[compliance: FTC header]
    E --> F[gemini_client + prompt review_v1]
    F --> G[Salvar .md + .html]
    G --> H[status = PRODUCED]
    H --> I[checklist publicação]
    I --> J{Publicado?}
    J -->|Sim| K[Registrar URL em metrics]
    J -->|Não| L[Backlog manual]
```

---

## 🔀 Fluxo de Decisão (Pivot)

```mermaid
flowchart TD
    M[Métricas Fase 4] --> V{Views >= 300?}
    V -->|Não| W[Continuar teste]
    V -->|Sim| C{CTR > 0?}
    C -->|Não| R[REJECTED - pivot nicho]
    C -->|Sim| S{Vendas > 0?}
    S -->|Sim| E[ESCALA - mais conteúdo]
    S -->|Não| A[Ajustar copy/CTA]
```

Ver thresholds completos em [13-metrics.md](./13-metrics.md).

---

## 🤖 Fluxo de Chamada IA

```
Request
  → hash_cache (MD5, TTL 7d) ──hit──→ Return
  → semantic_cache (cosine > 0.96) ──hit──→ Return
  → compress_context()
  → gemini.generate(structured_output=PydanticModel)
  → persist both caches
  → Return
```

**Proibido:** bypass direto ao Gemini sem passar por este fluxo.

---

*Última atualização: julho/2026*
