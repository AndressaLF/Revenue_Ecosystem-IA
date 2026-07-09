# 🌐 Visão — RE-IA

> Ecossistema de geração de renda baseado em IA que maximiza ROI e minimiza complexidade.

---

## 📑 Sumário

1. [Missão](#-missão)
2. [Posicionamento Estratégico](#-posicionamento-estratégico)
3. [O Que É (e O Que Não É)](#-o-que-é-e-o-que-não-é)
4. [Princípios Inegociáveis](#-princípios-inegociáveis)
5. [Audience Intelligence](#-audience-intelligence)
6. [Os 5 Pilares](#-os-5-pilares)
7. [Vantagem Competitiva (Moat)](#-vantagem-competitiva-moat)
8. [Framework de Decisão](#-framework-de-decisão)
9. [Filosofia de Execução](#-filosofia-de-execução)

---

## 🎯 Missão

Encontrar, validar e monetizar oportunidades digitais com **alta probabilidade de gerar receita em dólar em até 30 dias**, usando módulos Python independentes, dados públicos gratuitos e IA apenas onde agrega valor mensurável.

**Não promovemos produtos.** Promovemos **soluções para dores específicas de personas identificadas em dados reais** — o produto é consequência do score, não o ponto de partida.

---

## 🎪 Posicionamento Estratégico

### Sistema de decisão, não canal de promoção

| Multidão de afiliados | RE-IA |
|----------------------|-------|
| Escolhe 1 produto e divulga | Escolhe **persona + dor + canal**, depois o produto |
| Otimiza comissão % | Otimiza **EPC** (ganho por clique) |
| Um funil para tudo | Funil por vertical (SaaS ≠ template ≠ físico) |
| Insiste meses no produto errado | **Pivot com regra** (views, cliques, conversão) |
| Conteúdo genérico | Conteúdo por **Job-to-be-Done** |

### Mensagem de mercado

> *"Identificamos micro-oportunidades transacionais em mercados USD, validamos com score matemático (FCI/IEMA/EPC), publicamos só o que passa no filtro e abandonamos em dias — não meses — o que não converte."*

### Primeiro ciclo de 30 dias (recomendação estratégica)

Focar **apenas `02_affiliate_saas`** até a primeira comissão em dólar. O módulo `03_notion_funnel` entra no **segundo ciclo** — evita dividir energia de publicação no prazo crítico.

Detalhes: [01-roadmap](./01-roadmap.md)

---

## ✅ O Que É (e O Que Não É)

| É | Não é |
|---|-------|
| Laboratório de negócios modular | Plataforma monolítica |
| **Máquina de triagem por público e dor** | Lista de produtos para afiliar |
| Scripts CLI autocontidos por módulo | Microserviços com filas no MVP |
| Núcleo de pesquisa + validação compartilhado | App único que faz tudo |
| Documentação para o Cursor implementar | Código completo neste repositório de docs |
| Priorização por ROI e velocidade | Arquitetura enterprise antecipada |

---

## 🔒 Princípios Inegociáveis

1. **Validar antes de construir** — demanda medida antes de código.
2. **Receita antes de escala** — primeira comissão em dólar > features extras.
3. **Público antes de produto** — persona e dor vêm antes da escolha do ativo ([15-audience-intelligence](./15-audience-intelligence.md)).
4. **Determinismo antes de IA** — regras, cache, DuckDB; Gemini só no final.
5. **Custo operacional mínimo** — APIs gratuitas, processamento local, zero nuvem gerenciada no MVP.
6. **Módulos independentes** — cada oportunidade de negócio = módulo executável isolado.
7. **Reutilização máxima** — pesquisa, SEO, IA e compliance em `shared_components/`.
8. **Descarte rápido** — ideias fracas morrem cedo ([13-metrics](./13-metrics.md)).
9. **Um foco por vertical por semana** — evita paralisia de escolha (comportamento humano codificado).

---

## 🎯 Audience Intelligence

Camada estratégica entre **Pesquisa** e **Validação** — o diferencial do RE-IA face à multidão.

```
Dados brutos → Persona → Dor → JTBD → Intenção → Score → Produção
```

| Conceito | O que é | Exemplo |
|----------|---------|---------|
| **Persona** | Quem sofre a dor | `freelancer`, `developer`, `home_consumer` |
| **Dor (Pain)** | Problema em linguagem real | "caos de clientes", "setup demorado no Cursor" |
| **Job-to-be-Done** | Progresso que o comprador busca | "Organizar clientes sem CRM de $99/mês" |

### Ciclo operacional

- **3× por semana** (seg/qua/sex): ingestão → extração de dor → classificação → score → **top 3** oportunidades
- Humano aprova **1** em 15–30 min; código faz o resto

### Documentação completa

→ [15-audience-intelligence.md](./15-audience-intelligence.md) — pipeline formal, persona/dor, heurísticas H-01…H-14, vieses seguros, **Definition of Done (L1/L2/L3)**  
→ [06-apis.md](./06-apis.md) — ferramentas gratuitas EN/USD e matriz de enriquecimento de campos  
→ [14-deploy.md](./14-deploy.md) — automação 3×/semana (Task Scheduler vs GitHub Actions)

---

## 🏛️ Os 5 Pilares

| Pilar | Capacidade | Implementação MVP |
|-------|------------|-------------------|
| **1 — Pesquisa** | Nichos, tendências, keywords, **dores**, personas | `01_opportunity_finder` + fontes gratuitas |
| **1.5 — Audience Intelligence** | Persona, dor, JTBD, canal sugerido | `01` subpacote `audience/` |
| **2 — Validação** | FCI, IEMA, EPC, Opportunity Score | Filtros DuckDB + Gemini estruturado |
| **3 — Produção** | Reviews, templates, funis (por JTBD) | `02_affiliate_saas`, `03_notion_funnel` |
| **4 — Publicação** | Ponte obrigatória (Medium/YouTube) → afiliado | Checklists; nunca link bruto em Reddit/Pinterest |
| **5 — Monitoramento** | EPC por canal/persona; pivots | Streamlit local (Fase 4) |

> Pilares 1, 1.5 e 2 são **obrigatórios** antes de produção.

---

## 🏰 Vantagem Competitiva (Moat)

Elementos que sustentam diferenciação além de "escolher produto e postar":

| Moat | Descrição | Implementação |
|------|-----------|---------------|
| **Memória acumulada** | Histórico do que converteu por persona/canal/vertical | SQLite `opportunities` + `metrics` |
| **Descarte rápido** | Custo baixo de testar; pivot em dias | Regras [13-metrics](./13-metrics.md) |
| **Ponte obrigatória** | Medium/YouTube antes do link; FTC + sub-IDs | `02`/`03` + `compliance/` |
| **Score matemático** | FCI/IEMA/EPC > intuição | `01` rank |
| **pSEO programático** | `[Profissão] × [Ativo]` em escala | Backlog pós-receita [11-backlog](./11-backlog.md) |
| **Lista própria** | E-mail/Substack para receita recorrente | Pós-MVP (playbooks enfatizam) |

### O que NÃO construir no MVP (distração)

- Módulo permanente de "caça a ferramentas de pesquisa em alta"
- Múltiplos módulos de produção em paralelo no 1º ciclo de 30 dias
- IA em loop de ingestão diária sem filtro

Atualizar fontes em `06-apis.md` manualmente a cada trimestre é suficiente.

---

## 🧮 Framework de Decisão

Para qualquer nova ideia, produto ou feature:

| # | Pergunta | Descarte se |
|---|----------|-------------|
| 1 | Existe **dor** comprovada em dados (Reddit, PH, Trends)? | Não |
| 2 | **Persona** identificável com hábito de pagar em USD? | Não |
| 3 | Existe intenção de compra (cauda longa transacional)? | Não |
| 4 | Concorrência baixa ou KD viável? | Não |
| 5 | Lançável em < 30 dias? | Não |
| 6 | EPC estimado > mínimo da vertical? | Não |
| 7 | Canal orgânico gratuito viável para esta persona? | Não |
| 8 | ROI esperado positivo em 30 dias? | Não |
| 9 | Risco técnico/regulatório controlado? | Não |
| 10 | Vale construir vs. reutilizar módulo existente? | Não |

---

## 🔄 Filosofia de Execução

```
Descobrir → Entender público → Validar → Vender → Construir → Escalar
              (Audience Intelligence)
```

| Papel | Responsabilidade |
|-------|------------------|
| **Arquiteto** | Visão, priorização, documentação |
| **Cursor** | Implementação incremental ([08-cursor](./08-cursor.md)) |
| **Humano** | Aprovar top 3, testar produto, publicar, revisar copy crítica |

**Próximos passos:**

1. [15-audience-intelligence.md](./15-audience-intelligence.md) — especificação da camada
2. [01-roadmap.md](./01-roadmap.md) — fases e metas
3. [03-modules.md](./03-modules.md) — implementação no `01`

---

*Última atualização: julho/2026*
