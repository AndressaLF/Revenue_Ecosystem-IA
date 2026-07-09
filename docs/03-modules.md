# 🧩 Módulos — Especificação e Alinhamento de Negócio

> Cada módulo = laboratório de negócio independente. Regras abaixo derivam dos [playbooks smart/](./smart/README.md).

**Referências:** [Arquitetura](./02-architecture.md) · [Fluxos](./04-flows.md) · [Métricas](./13-metrics.md) · [Monetização](./10-monetization.md)

---

## 📑 Sumário

1. [Contrato Comum](#-contrato-comum)
2. [01 — Opportunity Finder](#-01--opportunity_finder)
3. [02 — Affiliate SaaS](#-02--affiliate_saas)
4. [03 — Notion Funnel](#-03--notion_funnel)
5. [04 — Physical Affiliate *(futuro)*](#-04--physical_affiliate-futuro)
6. [Módulos Futuros](#-módulos-futuros)

---

## 📜 Contrato Comum

```bash
python -m modules.<nome>.cli --help
python -m modules.<nome>.cli <comando> [opções]
```

| Requisito | Detalhe |
|-----------|---------|
| **Entrada** | SQLite, flags CLI, JSON exportado do `01` — nunca outro módulo |
| **Saída** | `output/` + SQLite + `metrics` quando publicado |
| **Vertical** | Campo `vertical` define qual playbook e framework aplicar |
| **Sub-IDs** | Todo link gerado: `?ref=<channel>_<opportunity_id>` |
| **Compliance** | FTC disclosure em **todo** HTML público |

```python
class ModuleResult(BaseModel):
    module: str
    opportunity_id: str | None
    vertical: str | None
    status: Literal["success", "skipped", "error"]
    output_path: Path | None
    tokens_used: int = 0
    business_score: float | None = None  # FCI, IEMA ou matriz 0-100
    message: str = ""
```

---

## 🔍 01 — opportunity_finder

**Pilares:** 1 (Pesquisa) + 1.5 (Audience Intelligence) + 2 (Validação)  
**Playbooks:** [todos](./smart/README.md)  
**Prioridade:** 🥇 Primeiro — sem ele, módulos 02/03 operam no escuro  
**Audience Intelligence:** [15-audience-intelligence](./15-audience-intelligence.md)

### Lógica de negócio (dos playbooks)

| Princípio | Implementação |
|-----------|---------------|
| **EPC > comissão %** | Calcular `estimated_epc` e persistir; usar no ranking |
| **Cauda longa transacional** | Regex: `alternative to`, `template for`, `vs`, `worth it`, `best * for` |
| **Intenção > volume bruto** | Penalizar keywords genéricas (`tips`, `how to` sem modificador comercial) |
| **Descarte rápido** | ~90% REJECTED antes da IA |
| **Uma vertical por oportunidade** | `vertical`: `saas` \| `template` \| `digital` \| `physical` |
| **Público antes de produto** | `persona_tag`, `pain_statement`, `jtbd_statement` antes do score final |
| **Um foco por vertical/semana** | Bloquear novo VALIDATED se já existe foco ativo na mesma vertical |

### Comandos CLI e resultados esperados

| Comando | O que faz | Resultado esperado (MVP) |
|---------|-----------|--------------------------|
| `ingest --source trends,reddit,producthunt` | Coleta dados gratuitos | ≥ 20 registros `PENDING`/execução; DuckDB populado |
| `ingest --source autosuggest,pinterest` | Cauda longa templates | ≥ 10 keywords com modificador transacional |
| `extract-pain` | Extrai dores de Reddit/PH | ≥ 20 sinais em `pain_signals`; `pain_category` preenchido |
| `classify-persona` | Persona + JTBD por cluster | `persona_tag`, `jtbd_statement` em oportunidades |
| `filter` | Hard-fail determinístico | ≥ 85% viram `REJECTED`; log de `reject_reason` |
| `score [--use-ai] [--vertical saas]` | Score + framework vertical | Top 5 com `opportunity_score` ≥ 65; FCI/IEMA calculado |
| `rank --vertical template --limit 10` | Ranking por EPC/FCI/IEMA | Lista ordenada para escolha humana |
| `rank --by audience` | Ranking persona × dor × intent | Top 3 para decisão humana semanal |
| `weekly-cycle` | Pipeline completo 3×/semana | ingest → pain → persona → filter → score → top 3 JSON |
| `list --status VALIDATED` | Fila de produção | 3–10 oportunidades prontas/semana após rotina |
| `export --id <id> --format json` | Handoff para 02/03 | JSON com persona, dor, JTBD + scores |

### Filtros hard-fail (automáticos)

| Regra | Vertical | Motivo (playbook) |
|-------|----------|-------------------|
| `search_volume < 500` | template/digital | Cauda longa OK com volume menor |
| `search_volume < 1000` | saas, physical | Mínimo para SaaS/físico |
| `competition_score > 50` | todas | KD proxy alto |
| Keyword só informativa | todas | Sem intenção de compra |
| `cookie_days < 30` | template/digital | Gumroad mínimo |
| `cookie_days < 60` | saas | B2B precisa 60–90d |
| `estimated_price` fora da zona | template | Fora $9–$29 → flag, não hard-fail |
| `estimated_price` fora $35–$100 | physical | Zona de impulso físico |
| `refund_rate > 8%` | physical | Estornos destroem margem |
| Duplicata keyword+source | todas | Deduplicação |

### Opportunity Score (0–100) + frameworks verticais

**Score base:**

| Fator | Peso | Fonte |
|-------|------|-------|
| Intenção transacional | 30% | Regex + Autosuggest |
| Volume / tendência | 25% | Trends, DuckDB |
| Concorrência (inversa) | 20% | KD proxy |
| Margem / EPC estimado | 15% | Preço × comissão × conversão estimada |
| Fit vertical (cookie, PLG, clone 1-click) | 10% | Metadados ingestão |

**FCI** (micro-ativos) — [micro_assets](./smart/micro_assets.md):

$$\text{FCI} = \frac{\text{Preço} \times \text{Comissão\%} \times \text{Nota LP (1-5)}}{\text{KD} \times \text{Fricção (1-5)}}$$

- VALIDATED se `opportunity_score ≥ 65` **e** `FCI ≥ 0.15` (calibrar com dados reais)
- `friction_score`: 1 = clone Notion/Sheets; 5 = zip pesado

**IEMA** (SaaS) — [saas_microsaas](./smart/saas_microsaas.md):

$$\text{IEMA} = \frac{\text{ARPU} \times \text{Comissão\%} \times (1 - \text{Churn})}{\text{KD}}$$

- VALIDATED se `opportunity_score ≥ 65` **e** `IEMA ≥ 0.5` (exemplo playbook: B=0.784)
- Penalizar: marcas saturadas (HubSpot, Zoom), freemium sem atribuição, wrappers IA

**Físicos** (pré-validação para módulo 04):

- Matriz playbook > 80 → prioridade; EPC estimado > $0.40

### Sinais de ingestão por vertical

| Vertical | Fontes prioritárias | Padrões de keyword |
|----------|---------------------|-------------------|
| `saas` | Product Hunt, Reddit r/SaaS, HN | `[nome] vs`, `alternatives`, `review` |
| `template` | Autosuggest, Etsy, Pinterest Trends, Reddit r/Notion | `template for [profissão]`, `notion CRM` |
| `digital` | Gumroad discover, Creative Market | `[ferramenta] boilerplate`, `prompt book` |
| `physical` | Amazon BS/M&S *(manual+futuro API)* | `best [produto] for [contexto]` |

### Ferramentas / componentes a implementar

| Componente | Path |
|------------|------|
| Conectores ingestão | `ingest/trends.py`, `reddit.py`, `producthunt.py`, `autosuggest.py` |
| Motor de filtros | `filter/rules.py` + config YAML por vertical |
| Calculadoras FCI/IEMA | `score/vertical_scoring.py` |
| Heurísticas intenção | `filter/intent_classifier.py` |
| Export schema | `schemas.py` |

### Critérios de aceite (técnicos + negócio)

- [ ] ≥ 90% descartados sem IA em `filter`
- [ ] `rank --vertical saas` ordena por IEMA
- [ ] `rank --vertical template` ordena por FCI
- [ ] Nenhuma keyword puramente informativa em VALIDATED
- [ ] `export` inclui `affiliate_url`, `keywords`, `framework_scores`
- [ ] **Audience Intelligence L1** antes de handoff produção — [15 § DoD](./15-audience-intelligence.md#-definition-of-done--completo-o-suficiente): Q1–Q4 + campos obrigatórios

---

## 💼 02 — affiliate_saas

**Playbook:** [saas_microsaas.md](./smart/saas_microsaas.md)  
**Pilares:** 3 (Produção) + 4 (Publicação)  
**Funil:** `YouTube/Medium (ponte)` → `link afiliado` — **nunca** link bruto no Reddit

### Lógica de negócio crítica

| Regra playbook | Implementação |
|----------------|---------------|
| Triângulo de ferro: Churn, ARPU, Cookie | Validar na ingestão; exibir no artigo |
| Conteúdo = caso de uso, não features | Prompt `review_v1` força estrutura Jobs-to-be-Done |
| Keywords fundo de funil | `Alternative to X`, `Is X worth it`, `X vs Y` |
| 1 SaaS por artigo | CLI rejeita batch misto no mesmo output |
| Aha Moment nos primeiros 90s | Checklist YouTube (humano) |
| Cookie 60–90d | Alerta se `cookie_days < 60` no meta.json |
| Evitar 5 CRMs no mesmo post | Um produto foco + menção comparativa leve |

### Comandos e resultados esperados

| Comando | Resultado esperado (Fase 2) |
|---------|----------------------------|
| `produce --id <uuid>` | `{id}_review.md` + `.html` + `_meta.json`; status → PRODUCED |
| `produce` (qualidade) | Inglês natural; 2 contras honestos; FTC no topo; < 2000 tokens |
| `checklist --channel medium` | Markdown com passos: publicar, indexar, sub-ID |
| `checklist --channel youtube` | Roteiro 5–8 min; gancho 90s; link no comentário fixado |
| `batch --limit 3` | 3 artigos; cache IA; nunca mesmo SaaS duplicado |

### Estrutura de saída

```
modules/02_affiliate_saas/output/
├── {id}_review.md          # Medium/Substack
├── {id}_review.html        # Blog próprio / Google Sites
├── {id}_meta.json          # SEO, FTC, keywords, sub-IDs
├── {id}_youtube_script.md  # Opcional: roteiro tutorial
└── {id}_publish_checklist.md
```

### `_meta.json` mínimo

```json
{
  "opportunity_id": "...",
  "product_name": "Example SaaS",
  "affiliate_url": "https://...?ref=medium_abc123",
  "keywords": ["x alternative", "x review"],
  "ftc_disclosure": "This post contains affiliate links...",
  "iema_score": 0.78,
  "cookie_days": 90,
  "expected_ctr": 0.03
}
```

### Resultados de negócio esperados (30 dias — playbook)

| Semana | Meta |
|--------|------|
| 1 | 2 programas afiliados aprovados; 2 oportunidades VALIDATED com IEMA ≥ 0.5 |
| 2 | 1 artigo Medium + 1 roteiro vídeo publicados |
| 3 | CTR link afiliado > **3%** (views → cliques painel) |
| 4 | ≥ 1 trial ou venda **ou** pivot se 300 cliques / 0 conversão |

### Ferramentas a implementar

| Ferramenta | Função |
|------------|--------|
| `templates/review.md.j2` | Estrutura Jinja2 do artigo |
| `compliance/ftc_disclosure.py` | Bloco obrigatório |
| `compliance/sub_id.py` | Gerador `?ref=channel_id` |
| Prompt `review_v1` | [07-prompts](./07-prompts.md) |
| `checklist/` | YAML por canal (medium, youtube, reddit) |

### Critérios de aceite

- [ ] HTML com FTC acima da dobra
- [ ] Foco em um único SaaS (comparativo leve OK)
- [ ] Keywords do export usadas no H1/H2
- [ ] `metrics` registrável com `channel=medium|youtube`

---

## 📝 03 — notion_funnel

**Playbook:** [micro_assets.md](./smart/micro_assets.md)  
**Pilares:** 3 (Produção) + 4 (Publicação)  
**Funil:** `Pinterest Pins` → `Medium (análise)` → `Gumroad/afiliado`

### Lógica de negócio crítica

| Regra playbook | Implementação |
|----------------|---------------|
| Ticket $9–$29 (impulso) | Validar `estimated_price` na entrada |
| Utilidade > educação | Spec = sistema pronto, não e-book teórico |
| Clone 1-click > download | `friction_score` preferir Notion/Sheets |
| pSEO: [Profissão] + [Ativo] | Gerar variantes de título no meta |
| Pinterest principal canal visual | Checklist 15 pins 2:3; 2–3/dia |
| Listas curadas convertem | Template `listicle` opcional no Medium |
| Gumroad cookie 30d+ | Verificar programa antes de PRODUCED |
| Não link afiliado direto no Pinterest/Reddit | Checklist reforça Medium como destino |

### Comandos e resultados esperados

| Comando | Resultado esperado (Fase 3) |
|---------|----------------------------|
| `produce --id <uuid>` | `template_spec.json` implementável em < 2h manual |
| `funnel --id <uuid>` | 3 e-mails + landing copy + tags Gumroad |
| `checklist --channel gumroad,pinterest` | Passo a passo publicação; 15 títulos de pin sugeridos |
| `pseo-variants --id <uuid>` | 5 títulos: `[Profissão] + [template type]` |

### Estrutura de saída

```
modules/03_notion_funnel/output/
├── {id}_template_spec.json   # Páginas, blocos, dummy data
├── {id}_landing_copy.md      # Headline, benefício tempo, CTA
├── {id}_email_sequence.md    # 3 e-mails funil
├── {id}_pin_titles.md        # 15 títulos Pinterest (gancho eficiência)
├── {id}_medium_article.md    # Análise / listicle
└── {id}_publish_checklist.md
```

### Nichos prioritários (playbook XIV)

Implementar tags de sugestão no `produce` para:

1. Cursor boilerplates · 2. ATS currículos · 3. CRM Notion freelancers · 4. Planilhas precificação · 5. Mockups POD

### Resultados de negócio esperados (30 dias)

| Semana | Meta |
|--------|------|
| 1 | 2 ativos FCI top; links afiliado com `?ref=pinterest_pinN` |
| 2 | 1 artigo Medium com prints internos + 2 limitações |
| 3 | 15 pins; impressões crescentes no Pinterest Analytics |
| 4 | CTR afiliado > **15%** OU pivot se < 50 cliques externos em 20 dias |

### Ferramentas a implementar

| Ferramenta | Função |
|------------|--------|
| `templates/notion_spec.schema.json` | Validação JSON spec |
| Prompt `notion_spec_v1`, `email_seq_v1` | [07-prompts](./07-prompts.md) |
| `pseo/title_generator.py` | Variantes profissão × ativo |
| `checklist/pinterest.md` | Formato 2:3, frequência, destino Medium |

### Critérios de aceite

- [ ] Spec com `pages[]`, `blocks[]`, `dummy_data_hints`
- [ ] Copy enfatiza tempo poupado (não design)
- [ ] Checklist proíbe link direto afiliado em pins
- [ ] FCI persistido no `meta` da oportunidade

---

## 📦 04 — physical_affiliate *(futuro)*

**Playbook:** [physical_products.md](./smart/physical_products.md)  
**Gate:** primeira receita em 02 ou 03  
**Módulo:** espelha estrutura do `02` com regras físicas

### Lógica pré-configurada (para ingestão já)

| Regra | Valor |
|-------|-------|
| Ticket | $35–$100 |
| Cookie Amazon | 24h → funil último clique; Medium obrigatório |
| CTR ponte | Meta 15–20% |
| Conversão Amazon | 4–10% |
| Refund rate | < 4% |
| Peso | < 2 kg preferido |
| Nichos MVP | Home Office Setup, Kitchen Gadgets |

### Resultado esperado quando implementado

- Review `best [product] for [context]` publicado
- 5–10 pins → Medium → Amazon Associates
- 3 vendas/semana = escalar; out of stock = pausar automático

---

## 🔮 Módulos Futuros

Ver [11-backlog.md](./11-backlog.md). Todos exigem `vertical` + playbook + ROI documentado.

| Módulo | Playbook | Framework |
|--------|----------|-----------|
| `05_ebook_factory` | micro_assets § VIII | Kit Ativação (ebook + template) |
| `06_seo_programmatic` | micro_assets § pSEO | `[Profissão] × [Ativo]` em escala |
| `07_micro_saas_mvp` | saas_microsaas | Validação manual + pré-venda |

---

*Última atualização: julho/2026 — alinhado aos playbooks smart/*
