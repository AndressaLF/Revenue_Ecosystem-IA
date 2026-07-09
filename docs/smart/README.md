# 📚 Playbooks de Mercado — Índice

> Inteligência de negócio que alimenta os módulos RE-IA. **Não duplicar aqui o que já está em código** — use esta pasta como fonte de regras e benchmarks.

---

## 🔗 Mapeamento Playbook → Módulo → Documentação Técnica

| Playbook | Vertical SQLite | Módulo de produção | Regras automatizadas | Funil principal |
|----------|-----------------|-------------------|----------------------|-----------------|
| [micro_assets.md](./micro_assets.md) | `template`, `digital` | `03_notion_funnel` | FCI, ticket $9–$29, KD<30 | Pinterest → Medium → Gumroad |
| [saas_microsaas.md](./saas_microsaas.md) | `saas` | `02_affiliate_saas` | IEMA, cookie≥60d, churn | YouTube/Medium → afiliado SaaS |
| [physical_products.md](./physical_products.md) | `physical` | `04_physical_affiliate` *(futuro)* | EPC, ticket $35–$75, refund<4% | Pinterest → Medium → Amazon |

**Motor comum:** `01_opportunity_finder` ingere, extrai **persona/dor/JTBD** ([15-audience-intelligence](../15-audience-intelligence.md)) e valida todas as verticais antes da produção.

**Specs técnicas:** [03-modules.md](../03-modules.md) · **Métricas:** [13-metrics.md](../13-metrics.md) · **Monetização:** [10-monetization.md](../10-monetization.md)

---

## 🧮 Frameworks de Triagem (implementar no módulo 01)

| Framework | Playbook | Fórmula | Uso no código |
|-----------|----------|---------|---------------|
| **FCI** | micro_assets | `(Preço × Comissão × Nota LP) / (KD × Fricção)` | `vertical IN (template, digital)` |
| **IEMA** | saas_microsaas | `(ARPU × Comissão × (1-Churn)) / KD` | `vertical = saas` |
| **Matriz 0–100** | todos | Pesos por critério | `opportunity_score` composto |
| **EPC** | todos | `Conversão LP × Comissão líquida` | Métrica de desempate |

**Threshold VALIDATED:** score ≥ 65 **e** framework da vertical acima do mínimo (ver [03-modules](../03-modules.md)).

---

## ✅ O Que Automatizar vs. Revisão Humana

| Origem (checklist 100 itens) | Automatizar no `01` | Humano obrigatório |
|------------------------------|---------------------|-------------------|
| Volume busca, KD, tendência | ✅ DuckDB + Trends | — |
| Intenção transacional (keyword) | ✅ Regex/heurísticas | — |
| Persona, dor, JTBD (Reddit/PH) | ✅ `extract-pain` + `classify-persona` | Aprovar 1 dos top 3/semana |
| Cookie duration, comissão % | ✅ Campos na ingestão | Confirmar no painel afiliado |
| Qualidade da LP, prova social | ⚠️ Parcial (meta scrape) | Testar produto antes de promover |
| Usabilidade do template/SaaS | ❌ | Testar antes de PRODUCED |
| Publicação em Pinterest/Reddit | ❌ | Checklist do módulo 02/03 |
| Copy em inglês nativo | ⚠️ IA + revisão | Revisar artigo crítico |
| FTC disclosure | ✅ `compliance/` | — |

---

## 📊 Resultados Esperados por Vertical (30 dias)

| Vertical | Meta financeira | CTR página ponte | Conversão | Pivot se |
|----------|-----------------|------------------|-----------|----------|
| Micro-ativos | 1ª venda Gumroad/afiliado | > 15% | EPC > $0,30 | < 50 cliques em 20 dias |
| SaaS | 1ª comissão trial/pago | > 3% clique afiliado | Trial > 0 após 50 cliques | 0% após 300 cliques |
| Físicos *(futuro)* | 3 vendas/semana | > 15–20% | 4–10% Amazon | 300 views sem clique |

---

*Leia o playbook da vertical antes de implementar ou operar o módulo correspondente.*
