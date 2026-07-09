# 📋 Backlog Priorizado por ROI

> Fila única de trabalho — Cursor implementa de cima para baixo.

**Referências:** [Roadmap](./01-roadmap.md) · [Módulos](./03-modules.md) · [Playbooks](./smart/README.md)

---

## 📑 Sumário

1. [Legenda](#-legenda)
2. [Sprint 0 — Infraestrutura](#-sprint-0--infraestrutura)
3. [Sprint 1 — Núcleo](#-sprint-1--núcleo)
4. [Sprint 2 — Receita SaaS](#-sprint-2--receita-saas)
5. [Sprint 3 — Receita Templates](#-sprint-3--receita-templates)
6. [Sprint 4 — Monitoramento](#-sprint-4--monitoramento)
7. [Backlog Futuro (Pós-receita)](#-backlog-futuro-pós-receita)

---

## 🏷️ Legenda

| Campo | Significado |
|-------|-------------|
| **P** | Prioridade (P0 = agora) |
| **ROI** | Impacto financeiro esperado (1–5) |
| **Effort** | Esforço (1 = horas, 5 = semanas) |
| **Score** | ROI ÷ Effort (maior = melhor) |

---

## 🔧 Sprint 0 — Infraestrutura

| P | Item | ROI | Eff | Score | Owner |
|---|------|-----|-----|-------|-------|
| P0 | Criar monorepo + `requirements.txt` | 3 | 1 | 3.0 | Cursor |
| P0 | `.gitignore` + `storage/` | 2 | 1 | 2.0 | Cursor |
| P0 | `.cursorrules` espelhando [08-cursor](./08-cursor.md) | 3 | 1 | 3.0 | Cursor |

---

## 🔍 Sprint 1 — Núcleo

| P | Item | ROI | Eff | Score | Doc |
|---|------|-----|-----|-------|-----|
| P0 | `shared_components/cache` | 5 | 2 | 2.5 | [02](./02-architecture.md) |
| P0 | `shared_components/database` | 5 | 2 | 2.5 | [05](./05-database.md) |
| P0 | `gemini_client` + compressão | 5 | 2 | 2.5 | [07](./07-prompts.md) |
| P0 | Ingest Trends + Reddit | 5 | 3 | 1.7 | [06](./06-apis.md) |
| P0 | Filtros determinísticos | 5 | 2 | 2.5 | [04](./04-flows.md) |
| P0 | `filter/intent_classifier.py` (transacional) | 5 | 2 | 2.5 | [smart/](./smart/README.md) |
| P0 | `audience/pain_extractor.py` | 5 | 2 | 2.5 | [15](./15-audience-intelligence.md) |
| P0 | `audience/persona_classifier.py` + JTBD | 5 | 2 | 2.5 | [15](./15-audience-intelligence.md) |
| P0 | `audience/enricher.py` + `enrichment_source` | 5 | 2 | 2.5 | [06](./06-apis.md) |
| P0 | `shared_components/audience/bias_guards.py` | 4 | 1 | 4.0 | [15](./15-audience-intelligence.md) |
| P0 | CLI `weekly-cycle` + `rank --by audience` | 5 | 2 | 2.5 | [15](./15-audience-intelligence.md) |
| P0 | `score/vertical_scoring.py` (FCI + IEMA + EPC) | 5 | 2 | 2.5 | [03](./03-modules.md) |
| P0 | CLI `01` ingest/filter/score/rank/export | 5 | 3 | 1.7 | [03](./03-modules.md) |
| P1 | Ingest Product Hunt + Autosuggest | 4 | 2 | 2.0 | [06](./06-apis.md) |
| P1 | `filter/rules.yaml` por vertical | 4 | 1 | 4.0 | [03](./03-modules.md) |
| P1 | Testes pytest core + scoring + audience | 4 | 2 | 2.0 | [09](./09-tests.md) |
| P1 | Agendar `weekly-cycle` 3×/semana (Task Scheduler) | 4 | 1 | 4.0 | [14](./14-deploy.md) |
| P2 | GitHub Actions CI (pytest only) | 3 | 1 | 3.0 | [14](./14-deploy.md) |
| P2 | GitHub Actions weekly-cycle + artifact | 3 | 2 | 1.5 | [14](./14-deploy.md) |

---

## 💼 Sprint 2 — Receita SaaS

| P | Item | ROI | Eff | Score | Doc |
|---|------|-----|-----|-------|-----|
| P0 | `compliance/ftc_disclosure` | 4 | 1 | 4.0 | [03](./03-modules.md) |
| P0 | Prompt `review_v1` | 5 | 1 | 5.0 | [07](./07-prompts.md) |
| P0 | CLI `02 produce` | 5 | 3 | 1.7 | [03](./03-modules.md) |
| P0 | Template HTML review (Jobs-to-be-Done) | 4 | 2 | 2.0 | [03](./03-modules.md) |
| P0 | `compliance/sub_id.py` | 4 | 1 | 4.0 | [03](./03-modules.md) |
| P0 | Checklists medium + youtube + reddit | 4 | 1 | 4.0 | [smart/saas](./smart/saas_microsaas.md) |
| P1 | `_youtube_script.md` opcional | 3 | 1 | 3.0 | [03](./03-modules.md) |
| P1 | Publicar 1º artigo (manual) | 5 | 1 | 5.0 | Humano |

---

## 📝 Sprint 3 — Receita Templates

| P | Item | ROI | Eff | Score | Doc |
|---|------|-----|-----|-------|-----|
| P0 | Prompt `notion_spec_v1` | 4 | 1 | 4.0 | [07](./07-prompts.md) |
| P0 | CLI `03 produce` + funnel | 4 | 3 | 1.3 | [03](./03-modules.md) |
| P0 | `pseo/title_generator.py` | 4 | 2 | 2.0 | [smart/micro](./smart/micro_assets.md) |
| P0 | `pin_titles.md` (15 ganchos 2:3) | 4 | 1 | 4.0 | [03](./03-modules.md) |
| P1 | Checklist Gumroad + Pinterest | 4 | 1 | 4.0 | [10](./10-monetization.md) |
| P1 | Publicar 15 pins (manual) | 5 | 2 | 2.5 | Humano |

---

## 📊 Sprint 4 — Monitoramento

| P | Item | ROI | Eff | Score | Doc |
|---|------|-----|-----|-------|-----|
| P0 | Tabela `metrics` + insert CLI | 4 | 2 | 2.0 | [05](./05-database.md) |
| P0 | Dashboard Streamlit | 4 | 2 | 2.0 | [13](./13-metrics.md) |
| P0 | Job pivot automático (REJECTED) | 5 | 1 | 5.0 | [13](./13-metrics.md) |

---

## 🔮 Backlog Futuro (Pós-receita)

> **Bloqueado** até primeira comissão em dólar.

| Item | ROI | Condição de desbloqueio |
|------|-----|-------------------------|
| `04_physical_affiliate` | 3 | 02 ou 03 com vendas |
| `05_ebook_factory` | 3 | 03 validado |
| `06_seo_programmatic` | 5 | 10+ artigos com tráfego |
| `07_micro_saas_mvp` | 5 | Oportunidade VALIDATED + pré-venda manual |
| Fila Redis/Celery | 2 | > 1000 oportunidades/dia |
| Chroma/FAISS vector store | 2 | Cache semântico > 100k entradas |
| Deploy cloud | 2 | MRR > $500/mês |

---

*Última atualização: julho/2026*
