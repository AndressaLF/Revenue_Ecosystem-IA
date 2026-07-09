# 🖱️ Cursor — Executor de Código

> Regras para o Cursor implementar o ecossistema incrementalmente.

**Espelhar em:** `.cursorrules` na raiz do repositório.  
**Arquitetura completa:** [02-architecture.md](./02-architecture.md)

---

## 📑 Sumário

1. [Papel do Cursor](#-papel-do-cursor)
2. [Ordem de Implementação](#-ordem-de-implementação)
3. [Configuração JSON](#-configuração-json)
4. [Padrões de Código](#-padrões-de-código)
5. [Checklist por PR / Sessão](#-checklist-por-pr--sessão)
6. [Proibições](#-proibições)

---

## 🎯 Papel do Cursor

| Faz | Não faz |
|-----|---------|
| Implementa módulos conforme [03-modules](./03-modules.md) | Decidir escopo de negócio |
| Escreve testes [09-tests](./09-tests.md) | Adicionar filas/eventos no MVP |
| Segue schemas [05-database](./05-database.md) | Chamar Gemini sem cache |
| Uma feature por sessão | Refatorar módulos inteiros de uma vez |

**Antes de codar:** ler doc relevante (00–14) + playbook `smart/` se módulo de produção.

---

## 📋 Ordem de Implementação

```
1. shared_components/cache
2. shared_components/database
3. shared_components/gemini_client
4. shared_components/compliance
5. modules/01_opportunity_finder (ingest → filter → score)
6. tests/ para cada camada acima
7. modules/02_affiliate_saas
8. modules/03_notion_funnel
9. dashboard Streamlit (Fase 4)
```

**Não pular etapas.** Módulo 02 só após 01 com critérios de aceite verdes.

---

## ⚙️ Configuração JSON

```json
{
  "project_type": "Python Modular Revenue Ecosystem",
  "architecture_style": "Clean Architecture / Highly Decoupled Plugins",
  "constraints": {
    "ai_cost": "Gemini must pass through semantic_cache + hash_cache",
    "similarity_threshold": 0.96,
    "local_embeddings": "sentence-transformers on CPU",
    "no_paid_apis_in_ingestion": true,
    "deterministic_first": true
  },
  "module_rules": {
    "standalone_cli": true,
    "shared_components_required": ["cache", "database", "compliance"],
    "pydantic_schemas": true,
    "no_cross_module_imports": true
  },
  "coding_standards": {
    "type_hints": "required",
    "docstrings": "Google style for public APIs",
    "tests": "pytest",
    "formatting": "black + isort"
  },
  "docs_canonical": "docs/00-vision.md through docs/14-deploy.md"
}
```

---

## 📐 Padrões de Código

```
modules/<nome>/
├── cli.py           # Typer ou argparse
├── schemas.py       # Pydantic
├── service.py       # Lógica de negócio
└── output/          # Gitignored artifacts
```

- Imports: `from shared_components.X import Y` — nunca `from modules.other`
- Config: `pydantic-settings` + `.env`
- Logs: `logging.getLogger(__name__)`

---

## ✅ Checklist por PR / Sessão

- [ ] Escopo de **uma** feature do [11-backlog](./11-backlog.md)
- [ ] Testes pytest passando
- [ ] Sem API paga na ingestão
- [ ] Gemini passa por `gemini_client` + cache
- [ ] Type hints + black/isort
- [ ] Atualizar doc só se contrato mudou

---

## 🚫 Proibições

| ❌ | Motivo |
|----|--------|
| DDD, CQRS, event bus no MVP | [12-risks](./12-risks.md) |
| Novo módulo sem entrada no backlog com ROI | Escopo |
| Dependência paga sem aprovação | Custo |
| Código sem teste em `shared_components` | Qualidade |
| Implementar 04+ antes de 02/03 validados | Priorização |

---

*Última atualização: julho/2026*
