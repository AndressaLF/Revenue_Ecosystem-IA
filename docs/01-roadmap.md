# 🗓️ Roadmap — 30 Dias por Impacto Financeiro

> Cada fase inclui **entregáveis técnicos** e **resultados de negócio** alinhados aos [playbooks smart/](./smart/README.md).

**Referências:** [Módulos](./03-modules.md) · [Monetização](./10-monetization.md) · [Métricas](./13-metrics.md)

---

## 📑 Sumário

1. [Priorização Financeira](#-priorização-financeira)
2. [Estratégia do Primeiro Ciclo](#-estratégia-do-primeiro-ciclo)
3. [Ciclo Operacional 3× por Semana](#-ciclo-operacional-3-por-semana)
4. [Visão das Fases](#-visão-das-fases)
5. [Fase 1 — Núcleo (Dias 1–5)](#-fase-1--núcleo-dias-15)
6. [Fase 2 — Afiliados SaaS (Dias 6–15)](#-fase-2--afiliados-saas-dias-615)
7. [Fase 3 — Infoprodutos (Dias 16–25)](#-fase-3--infoprodutos-dias-1625)
8. [Fase 4 — Monitoramento (Dias 26–30)](#-fase-4--monitoramento-dias-2630)
9. [Equipe por Fase](#-equipe-por-fase)

---

## 💰 Priorização Financeira

| Rank | Módulo | Playbook | Framework | Meta dia 30 |
|------|--------|----------|-----------|---------------|
| 🥇 | `02_affiliate_saas` | [saas_microsaas](./smart/saas_microsaas.md) | IEMA | 1ª comissão/trial SaaS |
| 🥈 | `03_notion_funnel` | [micro_assets](./smart/micro_assets.md) | FCI | 1ª venda digital |
| 🥉 | `04_physical` *(gate)* | [physical_products](./smart/physical_products.md) | Matriz >80 | Bloqueado |

---

## 🎯 Estratégia do Primeiro Ciclo

Recomendação da [Visão](./00-vision.md#-posicionamento-estratégico):

| Decisão | Motivo |
|---------|--------|
| **Foco em `02_affiliate_saas` até 1ª comissão** | Publicação manual é gargalo; dividir 02+03 atrasa receita |
| **`03_notion_funnel` no 2º ciclo** | Após validar funil SaaS e métricas EPC |
| **Audience Intelligence no Sprint 1** | Persona/dor antes do score — não escolher produto no escuro |

---

## 📅 Ciclo Operacional 3× por Semana

Após Fase 1, agendar `weekly-cycle` no módulo `01`:

| Dia | Comando | Meta |
|-----|---------|------|
| Segunda | `weekly-cycle` | Top 3 oportunidades ranqueadas |
| Quarta | `weekly-cycle` | Idem |
| Sexta | `weekly-cycle` + export | Top 3 + relatório persona/EPC |

Detalhes: [15-audience-intelligence](./15-audience-intelligence.md) · Agendamento: [14-deploy](./14-deploy.md) (**Task Scheduler recomendado no MVP**; GitHub Actions opcional pós-repo)

---

## 🗺️ Visão das Fases

```
Fase 1: 01_opportunity_finder (Audience Intelligence + FCI/IEMA/EPC)
    ↓ VALIDATED (top 3/semana → humano escolhe 1)
Fase 2: 02 → Medium/YouTube → afiliado SaaS  ← foco 1º ciclo
    ↓ 1ª comissão
Fase 3: 03 → Pinterest → Medium → Gumroad     ← 2º ciclo
    ↓
Fase 4: Métricas EPC + pivot automático
```

---

## 🏗️ Fase 1 — Núcleo (Dias 1–5)

### Entregáveis técnicos

| Item | Critério |
|------|----------|
| `shared_components` | cache, database, gemini_client, compliance |
| `01_opportunity_finder` | ingest, filter, score, rank, export |
| Audience Intelligence | `extract-pain`, `classify-persona`, `weekly-cycle` |
| Scoring vertical | FCI + IEMA + `estimated_epc` |
| Testes | pytest core ≥ 80% shared_components |

### Resultados de negócio esperados

| Métrica | Meta |
|---------|------|
| Oportunidades ingeridas | ≥ 50 na semana |
| Taxa rejeição filtro | ≥ 85% |
| VALIDATED | ≥ 5 com score ≥ 65 |
| SaaS com IEMA ≥ 0,5 | ≥ 2 candidatos |
| Templates com FCI ≥ 0,15 | ≥ 2 candidatos |
| Chamadas Gemini | < 50 total na fase |

### Não fazer

- Módulos 02/03, UI, Pinterest, publicação

---

## 💼 Fase 2 — Afiliados SaaS (Dias 6–15)

**Playbook:** [saas_microsaas](./smart/saas_microsaas.md) — funil YouTube/Medium → afiliado

### Entregáveis técnicos

| Item | Critério |
|------|----------|
| `02 produce` | .md + .html + meta.json + checklist |
| FTC + sub-IDs | Automático em toda saída |
| Prompt `review_v1` | Jobs-to-be-Done; < 2000 tokens |
| Checklists | medium, youtube, reddit |

### Resultados de negócio esperados

| Semana | Meta |
|--------|------|
| S1 (D6–8) | 2 programas afiliados aprovados; produce de 1 oportunidade IEMA top |
| S2 (D9–12) | 1 artigo Medium publicado; 1 roteiro vídeo (opcional publicar) |
| S2–S3 | CTR painel afiliado > **3%** (views artigo → cliques) |
| S4 (D13–15) | ≥ 1 trial **ou** venda **ou** decisão pivot documentada |

### Pivot (playbook)

- 300 cliques qualificados + 0 conversão → `REJECTED` + próximo SaaS da fila

---

## 📚 Fase 3 — Infoprodutos (Dias 16–25)

**Playbook:** [micro_assets](./smart/micro_assets.md) — funil Pinterest → Medium → Gumroad

### Entregáveis técnicos

| Item | Critério |
|------|----------|
| `03 produce` + `funnel` | spec JSON + e-mails + landing |
| `pseo-variants` | 5 títulos [Profissão]×[Ativo] |
| Checklist Pinterest | 15 pins 2:3; destino Medium |
| `pin_titles.md` | Ganchos de eficiência |

### Resultados de negócio esperados

| Semana | Meta |
|--------|------|
| S1 (D16–18) | 1 oportunidade FCI top → produce completo |
| S2 (D19–21) | Artigo Medium + Gumroad configurado |
| S3 (D22–24) | 15 pins publicados (2–3/dia) |
| S4 (D25) | CTR afiliado > **15%** **ou** pivot se < 50 cliques em 20 dias |

### Nichos sugeridos (playbook XIV)

Cursor boilerplates · CRM Notion freelancers · Planilhas precificação

---

## 📊 Fase 4 — Monitoramento (Dias 26–30)

### Entregáveis técnicos

| Item | Critério |
|------|----------|
| Dashboard Streamlit | Overview, canais, IA, alertas |
| `metrics` CLI | Registrar views, cliques, revenue |
| Pivot job | Auto REJECTED conforme [13-metrics](./13-metrics.md) |

### Resultados de negócio esperados

| Entrega | Conteúdo |
|---------|----------|
| Relatório ROI | EPC por canal (medium, pinterest, youtube) |
| Decisão escala | Qual vertical/módulo dobrar esforço |
| Decisão pivot | Quais oportunidades abandonar |
| Meta final | **≥ $1 USD** comissão total **ou** plano revisado com dados |

---

## 👥 Equipe por Fase

### Fase 1 — Núcleo

| Papel | Foco playbook |
|-------|---------------|
| Data Engineer | Trends, Reddit, Product Hunt, Autosuggest |
| Python Engineer | FCI/IEMA/EPC em código |
| Software Architect | Schemas export 01→02/03 |

### Fase 2 — SaaS

| Papel | Foco playbook |
|-------|---------------|
| SEO Specialist | `[SaaS] vs`, alternatives, KD < 25 |
| Prompt Engineer | Review = caso de uso, não features |
| Copywriter | 2 contras honestos no artigo |

### Fase 3 — Templates

| Papel | Foco playbook |
|-------|---------------|
| Product Designer | Spec Notion = sistema pronto |
| Growth Hacker | Pinterest 2:3; Medium como ponte |
| Copywriter | Tempo poupado, não design |

### Fase 4

| Papel | Entrega |
|-------|---------|
| Data Analyst | Relatório EPC; funil por vertical |
| QA | Smoke test pipeline completo |

---

*Última atualização: julho/2026*
