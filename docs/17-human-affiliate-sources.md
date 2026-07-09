# 🤝 Fontes Humanas — Afiliados e Recebimento USD

> Contas ativas do operador e fluxo manual de pesquisa → import → publicação.

**Config:** [config/human_sources.yaml](../config/human_sources.yaml) · [config/affiliate_programs.yaml](../config/affiliate_programs.yaml)

---

## 📑 Sumário

1. [Status das Contas](#-status-das-contas)
2. [Comparativo Rápido](#-comparativo-rápido)
3. [Digistore24](#-digistore24)
4. [ClickBank](#-clickbank)
5. [Amazon Associates](#-amazon-associates)
6. [Nomad — Recebimento](#-nomad--recebimento)
7. [Rotina Semanal Humana](#-rotina-semanal-humana)
8. [CLI — Importar Oportunidades](#-cli--importar-oportunidades)
9. [Compliance](#-compliance)

---

## ✅ Status das Contas

| Plataforma | Status | Papel no RE-IA |
|------------|--------|----------------|
| **Digistore24** | ✅ Ativa | Marketplace digital — hoplinks, cookie longo |
| **ClickBank** | ✅ Ativa | Marketplace digital — gravity, comissão alta |
| **Nomad** | ✅ Configurada | Recebimento consolidado em **USD** |
| **Amazon Associates** | ⏳ Criar se foco físico | Produtos físicos — cookie 24h |

---

## ⚖️ Comparativo Rápido

| | Digistore24 | ClickBank | Amazon |
|---|-------------|-----------|--------|
| **Vertical** | `digital` | `digital` | `physical` |
| **Comissão** | 10–30% | 50–75% | 1–3% |
| **Cookie** | **180d** | **60d** | **24h** |
| **Funil** | Medium/YouTube → hoplink | Medium/YouTube → VSL/LP | Pinterest → Medium → Amazon |
| **Métrica chave** | Refund + LP EN | **Gravity ≥ 20** | Rating + reviews |
| **EPC típico** | Médio-alto | Alto se gravity OK | Baixo %, alto volume |
| **Payout** | Nomad | Nomad | Nomad / PayPal |

**Estratégia 30 dias com contas ativas:** priorizar **ClickBank ou Digistore24** para 1ª comissão USD rápida (comissão alta + cookie longo); usar **Amazon** em paralelo só se já tiver Associates aprovado.

---

## 🟢 Digistore24

### Onde pesquisar (humano)

1. Login: [Digistore24 App](https://www.digistore24-app.com)
2. **Marketplace → Affiliate** — categorias EN: business, self-help, health (com cuidado FTC)
3. Filtrar: comissão ≥ 20%, materiais de afiliado disponíveis, LP em inglês

### O que copiar para o sistema

| Campo | Onde achar |
|-------|------------|
| `product_name` | Nome no marketplace |
| `estimated_price` | Preço de venda |
| `commission_pct` | Painel do produto |
| `affiliate_url` | **Hoplink** com seu ID de afiliado |
| `refund_rate` | Estatísticas do produto (se visível) |

### Evitar

- Claims médicos agressivos (FDA)
- Produtos sem página em inglês
- Refund > 5%

---

## 🔵 ClickBank

### Onde pesquisar (humano)

1. Login: [ClickBank Marketplace](https://accounts.clickbank.com/marketplace.htm)
2. Ordenar por **Gravity** (mín. **20** para promover)
3. **Affiliate Tools** → hoplink, avg $/sale, commission %

### O que copiar

| Campo | Onde achar |
|-------|------------|
| `gravity` | Listagem marketplace |
| `estimated_price` | Avg $ per sale |
| `commission_pct` | Affiliate tools |
| `vendor_id` | URL / tools |
| `affiliate_url` | Hoplink gerado |

### Regras

| Gravity | Ação |
|---------|------|
| < 15 | ❌ Não importar |
| 20–40 | ✅ Testar |
| 40–120 | ✅ Ideal |
| > 120 | ⚠️ Saturação — ângulo único obrigatório |

---

## 📦 Amazon Associates

*(Se/conta aprovada — foco físico)*

1. [Movers & Shakers](https://www.amazon.com/gp/movers-and-shakers) / Best Sellers — Home Office
2. Preço **$35–75**, rating **≥ 4,2**, reviews **≥ 100**
3. Link via SiteStripe / Link Builder + tag de associado

Funil: **Pinterest → Medium → Amazon** (nunca link direto no pin).

---

## 💳 Nomad — Recebimento

| Programa | Configurar no painel |
|----------|---------------------|
| Digistore24 | Método de pagamento → PayPal/banco vinculado à Nomad |
| ClickBank | Payment preferences → alinhado ao recebimento USD |
| Amazon | International direct deposit / PayPal conforme região |

**Semanal:** reconciliar *pending* vs *paid* em cada painel; meta ≥ **$1 USD** total no dia 30.

---

## 📅 Rotina Semanal Humana

| Dia | Tarefa |
|-----|--------|
| **Segunda** | Digistore24 + ClickBank marketplace; Reddit EN valida dor |
| **Quarta** | `import-affiliate` (1–3 produtos); testar LP mobile |
| **Sexta** | Publicar Medium; sub-ID por canal; conferir cliques |

Detalhes: `config/human_sources.yaml`

---

## 💻 CLI — Importar Oportunidades

```bash
# ClickBank (gravity obrigatória para validação)
python -m modules.opportunity_finder.cli import-affiliate \
  --platform clickbank \
  --keyword "honest review weight loss program for busy moms" \
  --product-name "Example Program" \
  --price 47.00 \
  --affiliate-url "https://hop.clickbank.net/?affiliate=YOU&vendor=VENDOR" \
  --commission-pct 50 \
  --gravity 35 \
  --refund-rate 0.03 \
  --vendor-id VENDOR

# Digistore24
python -m modules.opportunity_finder.cli import-affiliate \
  --platform digistore24 \
  --keyword "digistore24 product review worth it" \
  --product-name "Example Digital Product" \
  --price 97.00 \
  --affiliate-url "https://www.digistore24.com/redir/YOUR_HOPLINK" \
  --commission-pct 25 \
  --cookie-days 180

# Amazon (físico)
python -m modules.opportunity_finder.cli import-affiliate \
  --platform amazon \
  --keyword "best under desk cable tray small desk" \
  --product-name "Cable Management Tray" \
  --price 42.99 \
  --affiliate-url "https://www.amazon.com/dp/ASIN?tag=YOURTAG" \
  --rating 4.5 \
  --reviews 250
```

Depois: `filter` → `score` → `rank` → `physical_affiliate produce` (ou módulo digital quando existir).

---

## ⚖️ Compliance

- **FTC disclosure** no topo de todo conteúdo com hoplink
- **Sub-ID** por canal (`medium_`, `youtube_`, `pinterest_`)
- **Nunca** hoplink bruto em Reddit/Pinterest
- **Saúde (DS24/CB):** sem prometer cura; disclaimers da plataforma + revisão humana

---

*Última atualização: julho/2026*
