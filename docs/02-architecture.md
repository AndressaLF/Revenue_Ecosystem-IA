# 🏛️ Arquitetura — RE-IA

> Clean Architecture simplificada: plugins CLI, componentes compartilhados, IA como último estágio.

**Referências:** [Módulos](./03-modules.md) · [Fluxos](./04-flows.md) · [Banco](./05-database.md)

---

## 📑 Sumário

1. [Decisões Arquiteturais](#-decisões-arquiteturais)
2. [Mapa dos 5 Pilares](#-mapa-dos-5-pilares)
3. [Estrutura de Pastas](#-estrutura-de-pastas)
4. [Shared Components](#-shared-components)
5. [Pipeline de Dados](#-pipeline-de-dados)
6. [Estratégia de Custo IA](#-estratégia-de-custo-ia)
7. [Evolução Futura (Pós-MVP)](#-evolução-futura-pós-mvp)

---

## ⚖️ Decisões Arquiteturais

| ID | Decisão | MVP | Pós-receita |
|----|---------|-----|-------------|
| ADR-01 | Linguagem Python 3.11+ | ✅ | — |
| ADR-02 | Clean Architecture **simplificada** (camadas lógicas, sem over-engineering) | ✅ | — |
| ADR-03 | Módulos CLI standalone | ✅ | — |
| ADR-04 | SQLite + DuckDB local | ✅ | — |
| ADR-05 | Sem filas, sem eventos, sem DDD tático | ✅ | Reavaliar se throughput exigir |
| ADR-06 | Gemini Pro só após cache + filtros | ✅ | — |
| ADR-07 | Proibido import entre módulos | ✅ | — |
| ADR-08 | Embeddings locais (sentence-transformers CPU) | ✅ | FAISS/Chroma se volume crescer |

---

## 🗺️ Mapa dos 5 Pilares

```
                    ┌─────────────────────────────────────┐
                    │         shared_components           │
                    │  cache │ database │ compliance │ IA │
                    └─────────────────┬───────────────────┘
                                      │
     Pilar 1+2          Pilar 3           Pilar 3+4         Pilar 5
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ 01_opportunity│  │02_affiliate  │  │03_notion     │  │ dashboard    │
  │   _finder    │  │   _saas      │  │   _funnel    │  │ (streamlit)  │
  │ Pesquisa     │  │ Produção     │  │ Prod.+Pub.   │  │ Monitoramento│
  │ Validação    │  │              │  │              │  │              │
  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

| Pilar | Responsável | Saída típica |
|-------|-------------|--------------|
| 1 Pesquisa | `01_opportunity_finder ingest` | `opportunities` status=PENDING |
| 1.5 Audience Intelligence | `extract-pain` → `classify-persona` | `persona_tag`, `pain_*`, `jtbd_statement` |
| 2 Validação | `01_opportunity_finder score` | status=VALIDATED ou REJECTED |
| 3 Produção | `02_*` / `03_*` | Markdown, HTML, JSON de template |
| 4 Publicação | Checklist + semi-automação | URL publicada ou checklist preenchido |
| 5 Monitoramento | `dashboard` / Fase 4 | Alertas, relatórios de pivot |

---

## 📁 Estrutura de Pastas

```
revenue_ecosystem/
├── .cursorrules              # Espelho de docs/08-cursor.md
├── README.md
├── requirements.txt
├── main.py                   # Orquestrador opcional (não obrigatório no MVP)
│
├── docs/                     # Governança (esta pasta)
│   ├── 00-vision.md … 15-audience-intelligence.md
│   └── smart/                # Playbooks de mercado
│
├── shared_components/
│   ├── cache/
│   │   ├── semantic_cache.py
│   │   └── hash_cache.py
│   ├── database/
│   │   ├── sqlite_repo.py
│   │   └── analytics_engine.py
│   ├── compliance/
│   │   ├── ftc_disclosure.py
│   │   └── seo_sanitizer.py
│   ├── audience/
│   │   ├── heuristics.py     # H-01 … H-14
│   │   └── bias_guards.py    # Tetos de boost, manual_review
│   ├── seo/                  # Meta tags, slug, schema.org (futuro)
│   └── gemini_client.py
│
├── modules/
│   ├── 01_opportunity_finder/
│   │   ├── cli.py
│   │   ├── ingest/
│   │   ├── audience/         # Persona, dor, JTBD, canal
│   │   ├── filter/
│   │   └── score/
│   ├── 02_affiliate_saas/
│   │   ├── cli.py
│   │   ├── templates/
│   │   └── output/
│   └── 03_notion_funnel/
│       ├── cli.py
│       ├── templates/
│       └── output/
│
├── storage/                  # .gitignore
│   ├── local_cache.db
│   └── analytics.duckdb
│
└── tests/
    ├── shared_components/
    └── modules/
```

---

## 🔧 Shared Components

| Pacote | Função | Usado por |
|--------|--------|-----------|
| `cache/` | Semântico (cosseno) + hash MD5 TTL 7d | Todos os módulos que chamam IA |
| `database/` | SQLite operacional + DuckDB OLAP | 01 (obrigatório), 02/03 (leitura) |
| `compliance/` | FTC affiliate disclosure, sanitização SEO | 02, 03 (saída pública) |
| `gemini_client.py` | Único gateway Gemini; compressão de contexto | 01 (score), 02/03 (produção) |

**Contrato:** módulos importam apenas de `shared_components`, nunca entre si.

---

## 🔄 Pipeline de Dados

```
INGEST → EXTRACT PAIN → CLASSIFY PERSONA/JTBD → NORMALIZE
    → FILTER (determinístico) → AGGREGATE (DuckDB)
    → SCORE (regras + IA opcional) → RANK (audience × EPC)
    → PERSIST (SQLite) → PRODUCE → OUTPUT
```

A camada **Audience Intelligence** (entre ingest e filter) é detalhada em [15-audience-intelligence](./15-audience-intelligence.md).  
Fluxos e diagramas em [04-flows.md](./04-flows.md).

---

## 💰 Estratégia de Custo IA

Meta: **Gemini Pro ≈ $0** nas fases iniciais; **Cursor** usado só para implementação incremental documentada.

| Camada | Mecanismo | Economia |
|--------|-----------|----------|
| 1 | Cache semântico (similaridade > 0,96) | ~100% tokens em prompts repetidos |
| 2 | Cache hash MD5 (TTL 7 dias) | Prompts idênticos |
| 3 | Filtro pré-IA (volume, concorrência, duplicatas) | ~90% das oportunidades nunca chegam ao LLM |
| 4 | Compressão (stop-words, limite chars) | Menos tokens por chamada |
| 5 | Batch + Pydantic structured output | Uma chamada, JSON válido |
| 6 | Prompts < 500 tokens ([07-prompts](./07-prompts.md)) | Custo previsível |

**Regra:** se regras DuckDB + regex resolvem, **não chame IA**.

---

## 🚀 Evolução Futura (Pós-MVP)

Somente após **receita comprovada** em pelo menos um módulo:

| Necessidade | Solução | Gatilho |
|-------------|---------|---------|
| Jobs agendados | `schedule` ou cron local | Ingestão diária automatizada |
| Fila de tarefas | Redis + RQ ou Celery | > 1000 oportunidades/dia |
| Eventos | Pub/sub interno | Múltiplos módulos reagindo em tempo real |
| DDD tático | Bounded contexts | Equipe > 3 devs no mesmo repo |
| Chroma/FAISS | Vector store dedicado | > 100k entradas em cache semântico |

---

*Última atualização: julho/2026*
