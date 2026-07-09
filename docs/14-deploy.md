# 🚀 Deploy e Ambiente

> MVP 100% local — automação semanal documentada com comparativo de ferramentas.

**Referências:** [Audience Intelligence](./15-audience-intelligence.md) · [APIs](./06-apis.md) · [Riscos](./12-risks.md)

---

## 📑 Sumário

1. [Filosofia de Deploy](#-filosofia-de-deploy)
2. [Requisitos Locais](#-requisitos-locais)
3. [Setup Inicial](#-setup-inicial)
4. [Execução Manual](#-execução-manual)
5. [Automação Semanal 3× por Semana](#-automação-semanal-3-por-semana)
6. [Comparativo: Task Scheduler vs cron vs GitHub Actions](#-comparativo-task-scheduler-vs-cron-vs-github-actions)
7. [Implementação Recomendada por Fase](#-implementação-recomendada-por-fase)
8. [Evolução Futura](#-evolução-futura)

---

## 🎯 Filosofia de Deploy

| MVP (agora) | Após 1ª receita |
|-------------|-----------------|
| Máquina local Windows/Linux | Pode adicionar GitHub Actions ou VPS |
| SQLite/DuckDB locais | Backup de `storage/` em artifact ou S3 |
| Automação local gratuita | CI só se repo tiver código e secrets |
| Sem Docker obrigatório | Docker se equipe > 1 |

**Regra:** não gastar em infra antes de receita — mas **automação local é grátis** e recomendada desde a Fase 1 estável.

---

## 💻 Requisitos Locais

| Item | Versão mínima |
|------|---------------|
| Python | 3.11+ |
| pip / venv | Atual |
| Espaço em disco | 2 GB |
| RAM | 8 GB (embeddings CPU) |
| Rede | APIs públicas EN + Gemini |
| SO | Windows 10+ ou Linux |

---

## ⚙️ Setup Inicial

```bash
cd revenue_ecosystem
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
mkdir storage storage/exports
python -m shared_components.database.init_db
```

### `.env.example`

```env
GEMINI_API_KEY=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
PRODUCTHUNT_TOKEN=
INGEST_LOCALE=en-US
INGEST_GEO=US
LOG_LEVEL=INFO
```

---

## 🖐️ Execução Manual

```bash
# Pipeline completo (equivalente a 1 ciclo semanal)
python -m modules.01_opportunity_finder.cli weekly-cycle \
  --sources trends,reddit,producthunt,autosuggest \
  --locale en-US --geo US --top 3 \
  --output storage/exports/

# Produção (após humano aprovar 1 ID)
python -m modules.02_affiliate_saas.cli produce --id <UUID>
```

---

## 📅 Automação Semanal 3× por Semana

### O que automatizar

| Job | Comando | Dias | Horário sugerido (BRT) |
|-----|---------|------|------------------------|
| `weekly-cycle` | ingest → pain → persona → enrich → score → top 3 | Seg, Qua, Sex | 08:00 |
| `weekly-report` | resumo persona/EPC em Markdown | Sex | 08:30 |
| Backup DB *(opcional)* | copiar `storage/*.db` | Sex | 09:00 |

### Script unificado (`scripts/weekly_cycle.sh`)

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source .venv/bin/activate

STAMP=$(date +%Y%m%d_%H%M)
python -m modules.01_opportunity_finder.cli weekly-cycle \
  --sources trends,reddit,producthunt,autosuggest \
  --locale en-US --geo US --top 3 \
  --output "storage/exports/weekly_${STAMP}.json" \
  2>&1 | tee "storage/logs/weekly_${STAMP}.log"

# Sexta: relatório extra
if [ "$(date +%u)" -eq 5 ]; then
  python -m modules.01_opportunity_finder.cli report \
    --input "storage/exports/weekly_${STAMP}.json" \
    --output "storage/exports/report_${STAMP}.md"
fi
```

### Windows (`scripts/weekly_cycle.bat`)

```bat
@echo off
cd /d %~dp0..
call .venv\Scripts\activate.bat
for /f %%i in ('powershell -Command "Get-Date -Format yyyyMMdd_HHmm"') do set STAMP=%%i
python -m modules.01_opportunity_finder.cli weekly-cycle --sources trends,reddit,producthunt,autosuggest --locale en-US --geo US --top 3 --output storage\exports\weekly_%STAMP%.json
```

---

## ⚖️ Comparativo: Task Scheduler vs cron vs GitHub Actions

| Critério | Task Scheduler (Windows) | cron (Linux) | GitHub Actions |
|----------|--------------------------|--------------|----------------|
| **Custo** | Grátis | Grátis | Grátis (2000 min/mês) |
| **Onde roda** | Seu PC ligado | Seu PC/servidor | Runners GitHub |
| **SQLite local** | ✅ Nativo | ✅ Nativo | ⚠️ Ephemeral — precisa artifact/cache |
| **Secrets (.env)** | Local | Local | GitHub Secrets |
| **PC desligado** | ❌ Não roda | ❌ Não roda | ✅ Roda na nuvem |
| **Rate limit IP** | Seu IP residencial | Seu IP | IP compartilhado GitHub |
| **Complexidade** | Baixa | Baixa | Média |
| **Melhor para MVP** | ✅ **Recomendado (Windows)** | ✅ Linux local | ⚠️ Só após código no GitHub |

### Recomendação oficial RE-IA

| Fase | Ferramenta | Motivo |
|------|------------|--------|
| **Sprint 1–2 (MVP)** | **Task Scheduler** (Windows) ou **cron** (Linux) | DB local, zero custo, sem perder SQLite entre runs |
| **Código no GitHub + timeboxed** | GitHub Actions para **pytest apenas** | CI de qualidade, não ingestão |
| **Pós-receita, PC off** | GitHub Actions **ou** VPS $5 (Hetzner) | Actions: artifact DB; VPS: SQLite persistente |
| **Não usar** | Actions para ingest pesada sem cache | Risco rate-limit + runner cold start |

### GitHub Actions — quando e como

**Use para:**
- `pytest` em cada push/PR
- `weekly-cycle` **somente se** persistir DB via cache/artifact ou DB remoto

**Não use como primeira opção** porque:
1. Runners são efêmeros — `storage/local_cache.db` não persiste entre jobs sem estratégia explícita.
2. IP compartilhado pode acionar rate limits em Reddit/Trends.
3. Secrets no GitHub exigem repo privado para keys.

### Workflow exemplo — CI (pytest)

`.github/workflows/ci.yml`:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -q
```

### Workflow exemplo — weekly-cycle (opcional, pós-MVP)

`.github/workflows/weekly-cycle.yml`:

```yaml
name: Weekly Cycle
on:
  schedule:
    - cron: "0 11 * * 1,3,5"   # 08:00 BRT (UTC-3) ≈ 11:00 UTC
  workflow_dispatch:            # run manual

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - name: Restore DB cache
        uses: actions/cache@v4
        with:
          path: storage/
          key: storage-${{ github.run_id }}
          restore-keys: storage-
      - name: Run weekly-cycle
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
          REDDIT_CLIENT_SECRET: ${{ secrets.REDDIT_CLIENT_SECRET }}
          PRODUCTHUNT_TOKEN: ${{ secrets.PRODUCTHUNT_TOKEN }}
        run: |
          mkdir -p storage/exports storage/logs
          python -m modules.01_opportunity_finder.cli weekly-cycle \
            --sources trends,reddit,producthunt,autosuggest \
            --locale en-US --geo US --top 3 \
            --output storage/exports/weekly.json
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: weekly-export-${{ github.run_number }}
          path: |
            storage/exports/
            storage/local_cache.db
          retention-days: 30
```

> **Nota:** cache entre runs no Actions é limitado — para produção séria de ingest, preferir **VPS com cron** após MRR > $500.

### Task Scheduler — setup Windows (recomendado MVP)

1. Criar `scripts/weekly_cycle.bat` (acima).
2. Abrir **Agendador de Tarefas** → Criar Tarefa Básica.
3. Nome: `RE-IA Weekly Cycle`.
4. Gatilho: Semanal → Segunda, Quarta, Sexta → 08:00.
5. Ação: Iniciar programa → caminho do `.bat`.
6. Marcar: "Executar estando o usuário conectado ou não".
7. Condição: "Acordar o computador para executar" (se laptop).

### cron — setup Linux

```cron
# crontab -e
0 8 * * 1,3,5 /path/to/revenue_ecosystem/scripts/weekly_cycle.sh
```

---

## 🗺️ Implementação Recomendada por Fase

| Fase | Automação | Ferramenta |
|------|-----------|------------|
| Fase 0 (docs) | Manual | — |
| Fase 1 (01 pronto) | Manual 1×/dia | CLI local |
| Fase 1 estável | **3×/semana** | Task Scheduler / cron |
| Código no GitHub | pytest em push | GitHub Actions CI |
| Pós-receita | ingest 24/7 ou PC off | VPS cron **ou** Actions + artifact |
| MRR > $500 | Dashboard + backup | VPS + restic/S3 |

---

## 🌩️ Evolução Futura

| Estágio | Gatilho | Ação |
|---------|---------|------|
| 1 — Local manual | MVP | CLI |
| 2 — Local agendado | 01 estável | Task Scheduler / cron |
| 3 — CI | Repo GitHub | Actions pytest |
| 4 — Ingest remota | PC off / MRR | VPS ou Actions+artifact |
| 5 — Container | Equipe > 1 | Docker Compose |

---

*Última atualização: julho/2026*
