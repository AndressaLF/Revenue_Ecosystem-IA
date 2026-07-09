# 💰 Monetização e Regras de Negócio

> Ponte entre [playbooks smart/](./smart/README.md) e implementação dos módulos.

**Referências:** [Módulos](./03-modules.md) · [Métricas](./13-metrics.md) · [Roadmap](./01-roadmap.md)

---

## 📑 Sumário

1. [Métrica Soberana: EPC](#-métrica-soberana-epc)
2. [Frameworks por Vertical](#-frameworks-por-vertical)
3. [Funis por Vertical](#-funis-por-vertical)
4. [Plataformas e Cookies](#-plataformas-e-cookies)
5. [Priorização MVP](#-priorização-mvp)
6. [Regras Operacionais](#-regras-operacionais)
7. [Resultados Esperados (30 dias)](#-resultados-esperados-30-dias)

---

## 📊 Métrica Soberana: EPC

**Earnings Per Click** supera comissão % isolada em todas as verticais.

$$\text{EPC} = \text{Taxa de Conversão da LP} \times \text{Comissão Líquida por Venda}$$

| Exemplo | Comissão | Conversão | EPC | Veredito |
|---------|----------|-----------|-----|----------|
| Template $15 × 50% | $7,50 | 6% | **$0,45** | ✅ Promover |
| eBook $47 × 30% | $14,10 | 1% | **$0,14** | ❌ Evitar |

O módulo `01` deve calcular `estimated_epc` e usá-lo no `rank`.

---

## 🧮 Frameworks por Vertical

| Vertical | Framework | Fórmula | Threshold VALIDATED | Playbook |
|----------|-----------|---------|---------------------|----------|
| Templates / digitais | **FCI** | `(Preço × Comissão × Nota LP) / (KD × Fricção)` | FCI ≥ 0,15 + score ≥ 65 | [micro_assets](./smart/micro_assets.md) |
| SaaS / Micro SaaS | **IEMA** | `(ARPU × Comissão × (1-Churn)) / KD` | IEMA ≥ 0,5 + score ≥ 65 | [saas_microsaas](./smart/saas_microsaas.md) |
| Físicos | **Matriz 0–100** | Pesos demanda, KD, margem, refund | > 80 prioritário | [physical_products](./smart/physical_products.md) |
| Todas | **Matriz 0–100** | Checklist ponderado | ≥ 75 produzir; < 50 descartar | Todos |

### Pesos críticos (automatizar no score)

**Micro-ativos:** KD (1,5), atrito entrega/clone (1,5), ticket $14–$24 (1,2), comissão (1,2)  
**SaaS:** churn (1,5), KD (1,5), comissão recorrente (1,2), cookie (1,2)  
**Físicos:** demanda transacional (1,5), KD (1,5), margem líquida USD (1,2)

---

## 🔗 Funis por Vertical

### ☁️ SaaS — [playbook](./smart/saas_microsaas.md)

```
Product Hunt / Reddit (pesquisa)
    → Artigo Medium + Tutorial YouTube (5–8 min, Aha em 90s)
    → Link afiliado (comentário fixado / CTA artigo)
    → Painel afiliado (trial/conversão)
```

| Canal | Papel | Regra |
|-------|-------|-------|
| YouTube | Educação + confiança | Retenção 60s > 40% |
| Medium | Ponte SEO | CTR afiliado > 3% |
| Reddit/Quora | Infiltração | **Só** link do vídeo/artigo — nunca afiliado bruto |
| LinkedIn | B2B opcional | Casos de uso executivos |

### 💎 Micro-ativos — [playbook](./smart/micro_assets.md)

```
Pinterest Trends / Etsy autosuggest (pesquisa)
    → 15 Pins 2:3 (destino = Medium, NÃO afiliado)
    → Artigo análise / listicle no Medium
    → Gumroad ou link afiliado creator
```

| Canal | Papel | Regra |
|-------|-------|-------|
| Pinterest | Atração visual | 2–3 pins/dia; título = ganho de tempo |
| Medium | Conversão | CTR > 15%; 2 limitações honestas |
| Reddit | Suporte | Auxílio técnico → link artigo |

### 📦 Físicos *(futuro)* — [playbook](./smart/physical_products.md)

```
Amazon BS/M&S → Review Medium/Google Sites → Pinterest → Amazon Associates
```

| Regra | Detalhe |
|-------|---------|
| Cookie 24h | Conteúdo de fundo de funil; decisão rápida |
| Efeito carrinho | ~40–50% comissões de itens adicionais |
| Conversão | 4–10% em tráfego qualificado |

---

## 🏪 Plataformas e Cookies

| Plataforma | Vertical | Comissão | Cookie | Módulo |
|------------|----------|----------|--------|--------|
| Gumroad | template/digital | 10–80% | 30d | 03 |
| Lemon Squeezy | template/SaaS tools | 15–70% | 60d | 02, 03 |
| PartnerStack/Rewardful | SaaS | 20–40% rec. | 60–90d | 02 |
| Amazon Associates | physical | 1–3% | **24h** | 04 |
| **Digistore24** *(conta ativa)* | digital | 10–30% | **180d** | humano + `import-affiliate` |
| **ClickBank** *(conta ativa)* | digital | 50–75% | **60d** | humano + `import-affiliate` |
| **Nomad** | payout | — | — | Recebimento USD (todas acima) |
| Product Hunt | pesquisa SaaS | — | — | 01 |

**Fluxo humano completo:** [17-human-affiliate-sources.md](./17-human-affiliate-sources.md)

**Regra de ingestão:** persistir `cookie_days`, `commission_pct`, `estimated_price` para cálculo FCI/IEMA/EPC.

---

## 🥇 Priorização MVP

```
1º 02_affiliate_saas   → IEMA alto, Product Hunt, comissão recorrente
2º 03_notion_funnel    → FCI alto, Pinterest, ticket impulso
─── gate: 1ª comissão USD ───
3º 04_physical         → EPC + efeito carrinho
4º 06_seo_programmatic → pSEO escala após 10+ artigos
5º 07_micro_saas_mvp   → só com pré-venda manual
```

---

## 📐 Regras Operacionais

1. **Uma oportunidade foco por semana** — evitar paralisia (playbook: não listar 5 CRMs)
2. **Testar ativo antes de PRODUCED** — humano valida usabilidade (não automatizável)
3. **Sub-ID obrigatório** — `?ref=<canal>_<opportunity_id>`
4. **FTC no topo** — todo HTML via `compliance/`
5. **Inglês nativo** — IA estrutura; humano revisa artigos críticos
6. **Tráfego EUA/UK/CA/AU/DE** — moedas fortes
7. **Descartar** modismos algorítmicos (packs Instagram/TikTok estética)
8. **Preferir** ferramentas em hipercrescimento (Cursor, Notion, Bolt, Lovable)

---

## 🎯 Resultados Esperados (30 dias)

### Consolidado do ecossistema

| Marco | Meta | Responsável |
|-------|------|-------------|
| Fim Fase 1 | ≥ 5 VALIDATED/semana; rank por vertical funcional | `01` + Cursor |
| Fim Fase 2 | 1ª comissão SaaS **ou** 1 trial pago | `02` + humano (publicação) |
| Fim Fase 3 | 1ª venda template/afiliado digital | `03` + Pinterest/Medium |
| Fim Fase 4 | Dashboard com EPC real por canal | Streamlit |

### Por vertical (se operando apenas uma)

| Vertical | Sucesso | Ajuste | Abandono |
|----------|---------|--------|----------|
| **SaaS** | Trial/venda; CTR afiliado > 3% | CTR < 3% com tráfego | 300 cliques, 0 conversão |
| **Micro-ativos** | Venda; CTR > 15% | Leituras sem clique | < 50 cliques em 20 dias |
| **Físicos** | 3 vendas/semana | Cliques sem venda (estoque?) | 300 views sem clique; refund > 10% |

### Receita mínima aceitável (MVP)

| Item | Valor |
|------|-------|
| Primeira comissão | ≥ **$1 USD** |
| EPC alvo (digital) | ≥ **$0,30** |
| EPC alvo (SaaS pós-50 cliques) | ≥ **$0,50** implícito |

---

*Última atualização: julho/2026*
