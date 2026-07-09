# 📊 Métricas e KPIs

> Thresholds alinhados aos [playbooks smart/](./smart/README.md) — por vertical quando aplicável.

**Referências:** [Monetização](./10-monetization.md) · [Módulos](./03-modules.md)

---

## 📑 Sumário

1. [KPIs Norte](#-kpis-norte)
2. [Métricas por Módulo](#-métricas-por-módulo)
3. [Benchmarks por Vertical](#-benchmarks-por-vertical)
4. [Thresholds de Decisão](#-thresholds-de-decisão)
5. [Alertas e Dashboard](#-alertas-e-dashboard)

---

## 🎯 KPIs Norte

| KPI | Meta MVP | Prazo |
|-----|----------|-------|
| 💵 Receita total USD | ≥ $1 | Dia 30 |
| 📈 VALIDATED/semana | ≥ 5 | Pós Fase 1 |
| 📰 Artefatos PRODUCED | ≥ 3 | Dia 25 |
| 🤖 Tokens Gemini/dia | < 100k | Contínuo |
| 💰 Custo infra | $0/mês | MVP |

---

## 📈 Métricas por Módulo

### `01_opportunity_finder`

| Métrica | Meta | Ação se falhar |
|---------|------|----------------|
| Ingest/dia | ≥ 10 PENDING | Adicionar fonte [06-apis](./06-apis.md) |
| Rejeição filtro | ≥ 85% | Revisar regras (muito frouxo) |
| Cache hit IA | ≥ 30% após semana 2 | Normal; aumentar TTL |
| IEMA top (saas) | ≥ 0,5 | Não produzir 02 até atingir |
| FCI top (template) | ≥ 0,15 | Não produzir 03 até atingir |
| `estimated_epc` médio VALIDATED | ≥ $0,25 | Repriorizar nicho |

### `02_affiliate_saas`

| Métrica | Meta playbook | Fonte |
|---------|---------------|-------|
| Tokens/artigo | < 2000 | ModuleResult |
| CTR afiliado (views→cliques) | **> 3%** | metrics + painel |
| Retenção vídeo 60s | **> 40%** | YouTube Analytics |
| Trial após 50 cliques | **> 0** | Painel afiliado |
| Conversão pós-300 cliques | > 0% | Pivot se zero |

### `03_notion_funnel`

| Métrica | Meta playbook | Fonte |
|---------|---------------|-------|
| CTR ponte (Medium) | **> 15%** | metrics |
| Cliques externos Pinterest | ≥ 50 em 20 dias | Pinterest Analytics |
| Pins publicados | 15 em 2 semanas | Checklist |
| Vendas / comissão | ≥ 1 | Gumroad/afiliado |

### `04_physical` *(futuro)*

| Métrica | Meta playbook |
|---------|---------------|
| CTR ponte | 15–20% |
| Conversão Amazon | 4–10% |
| Vendas/semana (escala) | ≥ 3 |
| Refund rate | < 4% (alerta se > 10%) |

---

## 🏷️ Benchmarks por Vertical

| Vertical | Métrica chave | Verde | Amarelo | Vermelho |
|----------|---------------|-------|---------|----------|
| **SaaS** | CTR afiliado | > 3% | 1–3% | < 1% |
| **SaaS** | IEMA | ≥ 0,5 | 0,3–0,5 | < 0,3 |
| **Micro-ativos** | CTR ponte | > 15% | 5–15% | < 5% |
| **Micro-ativos** | FCI | ≥ 0,15 | 0,08–0,15 | < 0,08 |
| **Físicos** | EPC | > $0,40 | $0,20–0,40 | < $0,20 |
| **Todas** | EPC real | > $0,30 | $0,10–0,30 | < $0,10 |

---

## 🔀 Thresholds de Decisão

| Situação | Threshold | Ação | Playbook |
|----------|-----------|------|----------|
| Sem tráfego | < 50 views em 14d | Revisar canal | físicos |
| CTA fraco (digital) | ≥ 300 views, CTR < 5% | Reescrever copy | micro_assets |
| CTA fraco (SaaS) | CTR afiliado < 3% | Revisar CTAs / Aha | saas_microsaas |
| Cliques sem venda | ≥ 50 cliques, 0 vendas | Produto/LP/estoque | todos |
| Pivot SaaS | 300 cliques, 0 conversão | REJECTED | saas_microsaas |
| Pivot micro-ativos | < 50 cliques em 20d pins | REJECTED | micro_assets |
| Escalar | ≥ 3 vendas/semana | Replicar estrutura | physical_products |
| Out of stock | Constante | Pausar divulgação | physical_products |
| Refund spike | > 10% | Abandonar produto | physical_products |
| Token spike | > 100k/dia | `--no-ai`; auditar | arquitetura |

---

## 🔔 Alertas e Dashboard

### Alertas Streamlit (Fase 4)

| ID | Condição | Severidade |
|----|----------|------------|
| `PIVOT_SAAS` | clicks ≥ 300 AND conversions = 0 | 🔴 |
| `PIVOT_TEMPLATE` | pinterest_clicks < 50 AND days ≥ 20 | 🔴 |
| `WEAK_CTA` | views ≥ 100 AND ctr < 5% | 🟡 |
| `WINNER` | epc > 0.50 | 🟢 |
| `DEAD_LINK` | affiliate_url HTTP 404 | 🔴 |
| `STOCK_OUT` | vertical=physical AND stock=false | 🔴 |

### Páginas dashboard

1. **ROI por vertical** — EPC, revenue, decisão escala/pivot
2. **Funil** — PENDING → VALIDATED → PRODUCED → $ 
3. **Canais** — medium, pinterest, youtube, reddit
4. **Frameworks** — distribuição FCI/IEMA das VALIDATED
5. **IA** — tokens_saved, cache hit rate

---

*Última atualização: julho/2026*
