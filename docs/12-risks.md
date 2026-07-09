# ⚠️ Riscos e Restrições

> O que pode dar errado, problemas críticos com solução e como o ecossistema se protege.

**Referências:** [Visão](./00-vision.md) · [Audience Intelligence](./15-audience-intelligence.md) · [Deploy](./14-deploy.md) · [Métricas](./13-metrics.md)

---

## 📑 Sumário

1. [Resumo Executivo](#-resumo-executivo)
2. [Problemas Críticos e Soluções](#-problemas-críticos-e-soluções)
3. [Riscos de Escopo](#-riscos-de-escopo)
4. [Riscos Técnicos](#-riscos-técnicos)
5. [Riscos Comerciais](#-riscos-comerciais)
6. [Riscos de Heurísticas e Vieses](#-riscos-de-heurísticas-e-vieses)
7. [Riscos de Automação](#-riscos-de-automação)
8. [Restrições Inegociáveis](#-restrições-inegociáveis)
9. [Decisões ADR Consolidadas](#-decisões-adr-consolidadas)

---

## 📋 Resumo Executivo

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Escopo gigante | Alta | Crítico | 3 módulos MVP + backlog bloqueado |
| Custo IA explosivo | Média | Alto | 4 camadas cache/filtro |
| Paralisia por docs | Média | Alto | Fase 0 timeboxed; depois só código |
| Zero receita em 30d | Média | Alto | Pivot rules [13-metrics](./13-metrics.md) |
| Banimento afiliado | Baixa | Alto | FTC compliance + sem links brutos |
| Score inflado por heurísticas | Média | Alto | Teto boost + H-14 confidence |
| DB perdido (Actions) | Média | Alto | Task Scheduler local no MVP |

---

## 🚨 Problemas Críticos e Soluções

Catálogo operacional — cada item tem **sintoma**, **causa** e **solução implementável**.

### PC-01 — Documentação sem código (paralisia)

| | |
|---|---|
| **Sintoma** | 30 dias passam; zero VALIDATED em produção |
| **Causa** | Fase 0 infinita; medo de implementar |
| **Solução** | Timebox Fase 0 → Sprint 0 imediato ([11-backlog](./11-backlog.md)); métrica: 1º `weekly-cycle` em 7 dias |
| **Dono** | Humano + Cursor |

### PC-02 — Gemini em loop de ingestão (custo tokens)

| | |
|---|---|
| **Sintoma** | Conta Gemini dispara; centenas de calls/dia |
| **Causa** | IA chamada em cada registro PENDING |
| **Solução** | Filtro determinístico → score só top 20; `--no-ai` default; cache semântico ([07-prompts](./07-prompts.md)) |
| **Dono** | `gemini_client.py` |

### PC-03 — Persona/dor inventados (sem fonte)

| | |
|---|---|
| **Sintoma** | Copy não ressoa; CTR zero com tráfego |
| **Causa** | Gemini alucina persona; sem `pain_signals` |
| **Solução** | `pain_statement` só de cluster Reddit; `persona_confidence < 0.5` → manual_review; link `source_url` no export |
| **Dono** | `audience/pain_extractor.py` |

### PC-04 — Escolher produto sem testar

| | |
|---|---|
| **Sintoma** | Conversão zero; reclamações; risco FTC |
| **Causa** | Afiliado promove sem usar o produto |
| **Solução** | Gate PRODUCED: checklist humano + `lp_quality_score` manual; proibido auto-publish |
| **Dono** | Humano |

### PC-05 — Paralisia por excesso de oportunidades

| | |
|---|---|
| **Sintoma** | 50 VALIDATED; nenhum publicado |
| **Causa** | Viés de sobrecarga de escolha |
| **Solução** | `weekly-cycle` exporta **top 3**; H-13 bloqueia 2º foco/vertical/semana |
| **Dono** | `heuristics.py` |

### PC-06 — Insistência no produto errado (sunk cost)

| | |
|---|---|
| **Sintoma** | 300+ views, 0 cliques; operador continua |
| **Causa** | Viés sunk cost humano |
| **Solução** | Pivot automático [13-metrics](./13-metrics.md): views ≥ 300 + CTR = 0 → REJECTED |
| **Dono** | Dashboard Fase 4 |

### PC-07 — Rate limit / ban IP (scraping)

| | |
|---|---|
| **Sintoma** | 429/403 em Reddit, Trends |
| **Causa** | Requests sem cache; IP Actions compartilhado |
| **Solução** | Cache 24h; 1 req/s; MVP em Task Scheduler local; OAuth Reddit oficial |
| **Dono** | Conectores ingest |

### PC-08 — SQLite perdido entre runs GitHub Actions

| | |
|---|---|
| **Sintoma** | Cada run começa DB vazio; sem memória acumulada |
| **Causa** | Runner efêmero |
| **Solução** | **MVP: Task Scheduler local**; Actions só com cache/artifact ou VPS |
| **Dono** | [14-deploy](./14-deploy.md) |

### PC-09 — Score inflado (heurísticas empilhadas)

| | |
|---|---|
| **Sintoma** | Tudo VALIDATED; nada converte |
| **Causa** | Boosts sem teto |
| **Solução** | Soma boosts ≤ 0.5; log `reject_reason`; calibrar com dados reais pós-30d |
| **Dono** | `bias_guards.py` |

### PC-10 — Conteúdo manipulativo (vício de marketing)

| | |
|---|---|
| **Sintoma** | Ban conta afiliado; reclamação FTC |
| **Causa** | Escassez falsa, depoimentos inventados |
| **Solução** | Checklist [15-audience — Vieses](./15-audience-intelligence.md#-usar-vieses-a-favor--sem-riscos-ao-negócio); disclosure automático |
| **Dono** | `compliance/` + humano |

### PC-11 — Mercado errado (PT-BR em vez de USD)

| | |
|---|---|
| **Sintoma** | Tráfego BR; comissão USD baixa |
| **Causa** | Fontes/canais em português |
| **Solução** | `INGEST_LOCALE=en-US`; filtrar não-EN; subreddits EN; Medium EN |
| **Dono** | Conectores + config |

### PC-12 — Dividir energia 02 + 03 no 1º ciclo

| | |
|---|---|
| **Sintoma** | Nada publicado com qualidade em 30d |
| **Causa** | Dois funis paralelos |
| **Solução** | 1º ciclo só `02_affiliate_saas` até 1ª comissão ([01-roadmap](./01-roadmap.md)) |
| **Dono** | Humano |

### PC-13 — Links brutos em Reddit/Pinterest

| | |
|---|---|
| **Sintoma** | Ban shadow; zero alcance |
| **Causa** | Afiliado posta URL direta |
| **Solução** | Ponte Medium/YouTube obrigatória; checklist canal |
| **Dono** | Módulos 02/03 |

### PC-14 — Campos schema vazios (enriquecimento falho)

| | |
|---|---|
| **Sintoma** | `persona_tag` null; score sem base |
| **Causa** | INGEST sem estágio ENRICH |
| **Solução** | `weekly-cycle` obrigatório estágios 1–4; matriz [06-apis](./06-apis.md#-matriz-de-enriquecimento-campo--ferramenta--método) |
| **Dono** | `audience/enricher.py` |

---

## 📦 Riscos de Escopo

| # | Risco | Mitigação |
|---|-------|-----------|
| 1 | Plataforma única para todos os modelos | Módulos independentes |
| 2 | Módulos sem ROI | [11-backlog](./11-backlog.md) gate pós-receita |
| 3 | Muitos especialistas no MVP | Máx. 2 papéis/fase |
| 4 | Documentar eternamente | Fase 0 encerra → Sprint 1 |
| 5 | Módulo "caça ferramentas trending" | Proibido no MVP ([00-vision](./00-vision.md)) |

---

## ⚙️ Riscos Técnicos

| # | Risco | Mitigação |
|---|-------|-----------|
| 5 | DDD/filas/eventos prematuros | ADR-05 |
| 6 | Scraping quebra / ban IP | Cache, rate limit, APIs oficiais |
| 7 | Gemini quota excedida | `--no-ai`; fila manual |
| 8 | Schema drift | Migrations versionadas |
| 9 | Acoplamento entre módulos | Linter + [08-cursor](./08-cursor.md) |
| 10 | Enrichment parcial | Validação Pydantic pós-enrich; log `enrichment_source` |

---

## 💼 Riscos Comerciais

| # | Risco | Mitigação |
|---|-------|-----------|
| 10 | Promover sem demanda | Score + VALIDATED + dor com fonte |
| 11 | CTR zero após tráfego | Pivot 300 views |
| 12 | Violação FTC | `ftc_disclosure` automático |
| 13 | Produto fora do ar | Monitorar links semanalmente |
| 14 | Concorrência saturada | Cauda longa EN + playbooks |
| 15 | Cookie curto SaaS | H-11 hard_reject |

---

## 🧠 Riscos de Heurísticas e Vieses

| # | Risco | Sintoma | Mitigação |
|---|-------|---------|-----------|
| H-R1 | Prova social falsa | Depoimentos inventados | Só dados com `source_url` |
| H-R2 | Boost excessivo | Tudo VALIDATED | Teto 0.5; calibração |
| H-R3 | Confirmação humana | Ignora REJECTED | Dashboard mostra `reject_reason` |
| H-R4 | Recência / hype | Perseguir trend sem dor | Exigir `pain_signals` ≥ 3 |
| H-R5 | Persona errada | Copy desalinhado | `persona_confidence` + manual_review |

Detalhes éticos: [15-audience — Vieses seguros](./15-audience-intelligence.md#-usar-vieses-a-favor--sem-riscos-ao-negócio).

---

## 🤖 Riscos de Automação

| # | Risco | Mitigação |
|---|-------|-----------|
| A-R1 | PC desligado; job não roda | Acordar PC ou VPS pós-receita |
| A-R2 | Actions sem DB persistente | Task Scheduler no MVP |
| A-R3 | Falha silenciosa no cron | Log em `storage/logs/` + notificação email opcional |
| A-R4 | Secrets expostos no repo | `.env` no `.gitignore`; Actions Secrets |

---

## 🔒 Restrições Inegociáveis

- ❌ Feature sem ROI no backlog
- ❌ API paga na ingestão (MVP)
- ❌ IA quando regras resolvem
- ❌ PRODUCED sem teste humano do produto
- ❌ Novo módulo antes de receita 02/03
- ❌ Trademark bidding / links brutos
- ❌ Escassez falsa / depoimentos inventados
- ❌ Publicar com `persona_confidence < 0.5` sem revisão

---

## ✅ Decisões ADR Consolidadas

| ID | Decisão |
|----|---------|
| ADR-01 | Python 3.11+ monorepo |
| ADR-02 | Clean Architecture simplificada |
| ADR-03 | `alpha_engine/` → `revenue_ecosystem/` |
| ADR-04 | Módulo 01 obrigatório primeiro |
| ADR-05 | Sem filas/eventos/DDD no MVP |
| ADR-06 | Gemini só via `gemini_client` + cache |
| ADR-07 | Fluxo: Descobrir → Audience → Validar → Vender |
| ADR-08 | Automação semanal: Task Scheduler MVP; Actions opcional |
| ADR-09 | Mercado alvo: USD / inglês (en-US) |

---

*Última atualização: julho/2026*
