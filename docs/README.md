# 🧭 RE-IA — Documentação Oficial do Ecossistema

> **Revenue Ecosystem IA** — Laboratório modular de oportunidades de renda com validação em 30 dias.

---

## 🎯 Comece Aqui

| Ordem | Documento | Para quem |
|-------|-----------|-----------|
| 00 | [Visão](./00-vision.md) | Todos — propósito, posicionamento, Audience Intelligence |
| 15 | [Audience Intelligence](./15-audience-intelligence.md) | Persona, dor, JTBD, **DoD L1/L2/L3** |
| 01 | [Roadmap](./01-roadmap.md) | TPM, CTO — fases, especialistas, priorização financeira |
| 02 | [Arquitetura](./02-architecture.md) | Arquiteto, engenheiros — pilares, pipeline, pastas |
| 03 | [Módulos](./03-modules.md) | Devs — especificação, CLI, contratos, handoffs |
| 04 | [Fluxos](./04-flows.md) | Todos — diagramas e sequências operacionais |

## 🔧 Engenharia

| # | Documento | Conteúdo |
|---|-----------|----------|
| 05 | [Banco de Dados](./05-database.md) | SQLite, DuckDB, schemas |
| 06 | [APIs e Fontes](./06-apis.md) | Ferramentas gratuitas EN/USD + matriz de enriquecimento |
| 07 | [Prompts](./07-prompts.md) | Estratégia de prompts e economia de tokens |
| 08 | [Cursor](./08-cursor.md) | Regras para o executor de código |
| 09 | [Testes](./09-tests.md) | Critérios de aceite e plano de testes |

## 💼 Negócio e Operação

| # | Documento | Conteúdo |
|---|-----------|----------|
| 10 | [Monetização](./10-monetization.md) | Modelos de receita e playbooks |
| 11 | [Backlog](./11-backlog.md) | Fila priorizada por ROI |
| 12 | [Riscos](./12-risks.md) | Problemas críticos (PC-01…14), heurísticas, automação |
| 13 | [Métricas](./13-metrics.md) | KPIs, alertas e pivots |
| 14 | [Deploy](./14-deploy.md) | Automação 3×/semana, Task Scheduler vs GitHub Actions |
| 17 | [Fontes Humanas](./17-human-affiliate-sources.md) | Digistore24, ClickBank, Amazon, Nomad (contas ativas) |
| 18 | [Secrets e .env](./18-secrets-and-env.md) | Chaves de API, `.env` seguro, prioridades P0–P3 |

> **Audience Intelligence** — resumo na [Visão](./00-vision.md#-audience-intelligence); especificação em [15](./15-audience-intelligence.md).

## 📚 Playbooks de Mercado

**Índice e mapeamento para código:** [smart/README.md](./smart/README.md)

| Documento | Nicho | Módulo | Framework |
|-----------|-------|--------|-----------|
| [Micro-Ativos](./smart/micro_assets.md) | Templates, e-books | `03_notion_funnel` | FCI |
| [SaaS / Micro SaaS](./smart/saas_microsaas.md) | Afiliados software | `02_affiliate_saas` | IEMA |
| [Produtos Físicos](./smart/physical_products.md) | Amazon/marketplaces | `04_physical` *(futuro)* | EPC |

---

## 📐 Regras de Navegação

1. **Um tema por arquivo** — use links, não cópias.
2. **Cursor implementa** — esta pasta orienta; não substitui código.
3. **MVP primeiro** — filas, eventos e DDD só após receita comprovada ([12-risks](./12-risks.md)).
4. **IA é último recurso** — regras e cache antes do Gemini ([02-architecture](./02-architecture.md)).

---

*Chief Architect deliverable — julho/2026*
