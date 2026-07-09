# 🤖 Estratégia de Prompts

> Prompts pequenos, estruturados e cacheáveis — Gemini e Cursor sob controle.

**Referências:** [Fluxos](./04-flows.md) · [Arquitetura](./02-architecture.md)

---

## 📑 Sumário

1. [Princípios](#-princípios)
2. [Inventário de Prompts](#-inventário-de-prompts)
3. [Template — Opportunity Score](#-template--opportunity-score)
4. [Template — Review SaaS](#-template--review-saas)
5. [Template — Template Notion](#-template--template-notion)
6. [Controle de Tokens](#-controle-de-tokens)

---

## 🎯 Princípios

1. **< 500 tokens** de input por chamada (após compressão)
2. **Structured output** via Pydantic — nunca pedir "texto livre longo"
3. **Versionar** prompts em `shared_components/prompts/{nome}_v{n}.txt`
4. **Cache obrigatório** — mesmo prompt + contexto = mesma resposta
5. **Cursor** recebe docs, não prompts gigantes — implementar por spec

---

## 📋 Inventário de Prompts

| ID | Uso | Módulo | Max tokens out |
|----|-----|--------|----------------|
| `score_v1` | Opportunity Score JSON | 01 | 300 |
| `review_v1` | Artigo review estruturado | 02 | 1500 |
| `notion_spec_v1` | Spec JSON do template | 03 | 800 |
| `email_seq_v1` | 3 e-mails de funil | 03 | 600 |

---

## 📊 Template — Opportunity Score

**Arquivo:** `shared_components/prompts/score_v1.txt`

```
Score this opportunity. Return JSON only.

Fields: ai_score (0-100), intent (transactional|informational),
risks (string[]), recommendation (pursue|reject|manual_review).

Context (compressed):
keyword: {keyword}
volume: {search_volume}
competition: {competition_score}
vertical: {vertical}
signals: {top_signals}
```

**Schema Pydantic:** `OpportunityScoreResult`

---

## 📝 Template — Review SaaS

**Arquivo:** `shared_components/prompts/review_v1.txt`

```
Write a balanced SaaS review. English. Return JSON.

Fields: title, meta_description, sections[{h2, body}],
pros[string[]], cons[string[]], cta_text, ftc_disclosure.

Product: {product_name}
Keywords: {keywords}
Competitors: {competitors}
Use case: {use_case}
Max words per section: 150.
```

**Pós-processamento:** `compliance/ftc_disclosure` injeta no HTML.

---

## 📋 Template — Template Notion

**Arquivo:** `shared_components/prompts/notion_spec_v1.txt`

```
Design a Notion template spec. Return JSON.

Fields: template_name, target_audience, pages[{name, blocks[]}],
dummy_data_hints, pricing_suggestion_usd, gumroad_tags[].

Keyword: {keyword}
Pain: {pain_point}
```

---

## 💰 Controle de Tokens

| Tática | Implementação |
|--------|---------------|
| Compressão | Remover stop-words; truncar `raw_data` a 500 chars |
| Batch | Agrupar até 5 keywords similares em uma chamada (futuro) |
| Memória longa | SQLite `ai_cache` — nunca repetir análise idêntica |
| Fallback | Se quota excedida → só regras determinísticas; fila manual |
| Métricas | Log `tokens_used` em `ModuleResult` |

**Meta diária MVP:** < 50 chamadas Gemini; < 100k tokens/dia.

---

*Última atualização: julho/2026*
