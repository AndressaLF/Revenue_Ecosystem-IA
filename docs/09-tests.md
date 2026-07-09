# 🧪 Testes e Critérios de Aceite

> Qualidade mínima para validar cada fase sem QA dedicado em tempo integral.

**Referências:** [Módulos](./03-modules.md) · [Cursor](./08-cursor.md)

---

## 📑 Sumário

1. [Estratégia de Testes](#-estratégia-de-testes)
2. [Testes por Componente](#-testes-por-componente)
3. [Critérios de Aceite por Fase](#-critérios-de-aceite-por-fase)
4. [Audience Intelligence — “Completo o Suficiente”](#-audience-intelligence--completo-o-suficiente)
5. [Smoke Test Manual](#-smoke-test-manual)

---

## 🎯 Estratégia de Testes

| Camada | Ferramenta | Cobertura mínima |
|--------|------------|------------------|
| `shared_components` | pytest + mocks | 80% |
| Filtros determinísticos | pytest parametrizado | 100% regras hard-fail |
| CLI módulos | pytest + `CliRunner` (typer) | happy path + 1 erro |
| Integração HTTP | `responses` / `httpx` mock | Conectores ingest |
| IA | Mock `gemini_client` | Nunca chamar API real em CI |
| E2E manual | Smoke script | Antes de cada fase |

---

## 🔬 Testes por Componente

### `semantic_cache`

- [ ] Retorna cache quando similaridade > 0,96
- [ ] Chama Gemini quando abaixo do threshold
- [ ] Persiste resposta para consulta futura

### `hash_cache`

- [ ] MD5 idêntico dentro de 7 dias → sem rede
- [ ] Expira após TTL

### `analytics_engine`

- [ ] Ingestão grava em DuckDB
- [ ] Agregação `keyword_stats` correta com fixture

### `01_opportunity_finder`

- [ ] `ingest` cria registros PENDING
- [ ] `filter` rejeita volume < 1000
- [ ] `score --no-ai` não chama Gemini
- [ ] `export` JSON válido contra schema

### `02_affiliate_saas`

- [ ] `produce` gera .md e .html
- [ ] FTC disclosure presente no HTML
- [ ] `tokens_used` registrado

### `03_notion_funnel`

- [ ] `produce` gera spec JSON válido
- [ ] Checklist Gumroad não vazio

---

## ✅ Critérios de Aceite por Fase

### Fase 1 — Núcleo

| Critério | Verificação |
|----------|-------------|
| CLI 01 funcional | `python -m modules.01_opportunity_finder.cli ingest` |
| ≥ 10 oportunidades ingeridas | Query SQLite |
| Filtro rejeita maioria | status REJECTED > 50% em teste |
| pytest green | `pytest tests/` |

### Fase 2 — SaaS

| Critério | Verificação |
|----------|-------------|
| 1 artigo gerado | Arquivo em `output/` |
| Publicável no Medium | Markdown renderiza |
| Link afiliado no CTA | HTML contém URL |

### Fase 3 — Notion

| Critério | Verificação |
|----------|-------------|
| Spec implementável | Revisão humana < 2h |
| Funil 3 e-mails | Arquivo `email_sequence.md` |

### Fase 4 — Monitoramento

| Critério | Verificação |
|----------|-------------|
| Dashboard local | Streamlit roda em localhost |
| Métricas persistidas | Tabela `metrics` populada |

---

## ✅ Audience Intelligence — “Completo o Suficiente”

Especificação completa: [15-audience-intelligence § Definition of Done](./15-audience-intelligence.md#-definition-of-done--completo-o-suficiente)

### Nível L1 (gate de produção — 1º ciclo 30 dias)

| # | Teste | Passa se |
|---|-------|----------|
| AI-L1-01 | Campos obrigatórios no export | `persona_tag`, `pain_statement`, `jtbd_statement`, `suggested_channel`, `intent_score`, `estimated_epc` preenchidos |
| AI-L1-02 | Persona mínima | `persona_tag` ≠ `unknown` e `persona_confidence` ≥ 0,5 |
| AI-L1-03 | Dor rastreável | ≥1 `pain_signals` com `source_url` **ou** `raw_data` contém URL |
| AI-L1-04 | Intenção | `intent_score` ≥ 0,35 |
| AI-L1-05 | Economia vertical | `status` = VALIDATED; EPC/framework conforme vertical |
| AI-L1-06 | Gate H-14 | Oportunidades com `persona_confidence` < 0,5 excluídas do top 3 |
| AI-L1-07 | Sem IA na classificação | `extract-pain` / `classify-persona` não chamam Gemini |

### Testes automatizados (pytest)

- [ ] Fixture oportunidade L1 passa validador `audience_sufficient()` *(implementar em `shared_components/audience/validators.py`)*
- [ ] `pain_statement` vazio → validador falha
- [ ] Import ClickBank `gravity` < 20 → `REJECTED` ([test_manual_marketplace](../tests/test_manual_marketplace.py))
- [ ] `produce` sem `affiliate_url` → CLI erro

### Smoke manual (antes de `produce`)

```bash
python -m modules.opportunity_finder.cli list --status VALIDATED
python -m modules.opportunity_finder.cli export --id <ID>
# Verificar JSON: Q1–Q4 em 15-audience-intelligence.md
```

---

## 🔥 Smoke Test Manual

```bash
# Fase 1
python -m modules.01_opportunity_finder.cli ingest --source trends,reddit
python -m modules.01_opportunity_finder.cli filter
python -m modules.01_opportunity_finder.cli score --use-ai --limit 3
python -m modules.01_opportunity_finder.cli list --status VALIDATED

# Fase 2
python -m modules.02_affiliate_saas.cli produce --id <UUID>

# Fase 3
python -m modules.03_notion_funnel.cli produce --id <UUID>
```

---

*Última atualização: julho/2026*
