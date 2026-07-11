# 🌐 RE-IA — Revenue Ecosystem IA

> *A friendly research lab for discovering and validating **USD affiliate opportunities** — powered by public data, smart scoring, and AI-assisted workflows.* ✨

[![Project status](https://img.shields.io/badge/status-active%20research-blue?style=flat-square)](https://github.com/AndressaLF/Revenue_Ecosystem-IA)
[![Live site](https://img.shields.io/badge/🌐_live_site-GitHub_Pages-purple?style=flat-square)](https://AndressaLF.github.io/Revenue_Ecosystem-IA/)
[![Market](https://img.shields.io/badge/market-USD%20%7C%20EN-green?style=flat-square)](#)
[![Ethics](https://img.shields.io/badge/ethics-FTC%20disclosure-orange?style=flat-square)](#-what-we-dont-do)

> 🇧🇷 Versão em português (Brasil): [README.pt-BR.md](README.pt-BR.md)

---

## 👋 Hi there!

**RE-IA** (*Revenue Ecosystem IA*) is a personal, open research project built to answer one question:

> *“Is there real buyer pain behind this affiliate opportunity — before I spend time creating content?”* 🤔

We combine **public market signals** (discussions, trends, intent keywords) with **deterministic scoring** and optional **AI drafts** — always with human review before anything goes live. No black-box hype. No spam. Just honest research. 💡

---

## 🎯 What RE-IA does

| Step | What happens |
|------|----------------|
| 🔍 **Discover** | Ingest public data (e.g. Reddit, Google Trends) |
| 🧠 **Understand** | Extract pain points & commercial intent |
| 📊 **Score** | Rank opportunities (EPC, audience fit, rules) |
| ✍️ **Draft** | Optional AI-assisted reviews + FTC disclosure |
| ✅ **Publish** | Human-approved content on owned channels (Medium, blog, etc.) |

Built for international (**EN / USD**) affiliate workflows — digital marketplaces & physical products.

---

## 🚫 What we *don’t* do

We’re researchers, not spammers. RE-IA will **never**:

- ❌ Post affiliate links directly on Reddit  
- ❌ Scrape private or logged-in content  
- ❌ Manipulate votes or automate posting  
- ❌ Ignore API rate limits (cached, throttled requests)  
- ❌ Skip **FTC affiliate disclosure** on published content  

Transparency matters. This repo exists partly so everyone — including API providers — can see exactly what we’re building. 🤝

---

## 🛠️ Tech stack

- 🐍 **Python 3.11+**
- 🗄️ **SQLite** (local research database)
- 🤖 **Multi-provider AI** (Gemini + Groq + Cerebras + OpenRouter) — free tier only
- 📋 YAML configs for affiliate rules & scoring

*Source code is developed locally; this public repo focuses on project documentation and transparency.*

> **Public mirror:** On GitHub you only get this README, [GitHub Pages](https://AndressaLF.github.io/Revenue_Ecosystem-IA/), and `.gitignore`. Full `docs/`, code, and the Streamlit dashboard stay in your **local clone** (see `.gitignore`).

### Documentation (local clone only)

| Topic | Local path |
|-------|------------|
| Human revenue guide | `docs/16-human-revenue-guide.md` |
| Operations (terminal) | `docs/19-operations.md` |
| Setup & `.env` | `docs/17-setup.md` |
| Medium publish | `docs/20-medium-manual-publish.md` |
| LLM gateway | `docs/21-llm-gateway.md` |
| **Dashboard (Streamlit)** | `docs/22-dashboard.md` |

📊 **Dashboard:** runs **only on your machine** — `python -m dashboard` → `http://localhost:8501`. It is **not** hosted on GitHub Pages (Pages serves the static site above).

---

## 💻 Quick start (local terminal)

```bash
# 1. Setup (first time)
python -m venv .venv
source .venv/Scripts/activate          # Git Bash on Windows
pip install -r requirements.txt
copy .env.example .env                 # then edit .env — NEVER commit it

# 2. Verify
python -m shared_components.config.check_env
python -m shared_components.database.init_db

# 3. Pipeline digital (recomendado — comece com dry-run)
python -m modules.opportunity_finder.cli plan-autopilot
python -m modules.opportunity_finder.cli run-autopilot --dry-run
# Quando estiver pronto:
python -m modules.opportunity_finder.cli run-autopilot --no-use-ai
python -m dashboard
```

> Commands are **Python modules**, not shell binaries — always prefix with `python -m`.

| Command | Purpose |
|---------|---------|
| `python -m shared_components.config.check_env` | Check `.env` keys + LLM chain |
| `python -m modules.opportunity_finder.cli plan-autopilot` | Preview seguro (só SQLite, sem rede) |
| `python -m modules.opportunity_finder.cli run-autopilot --dry-run` | Automação sem rede |
| `python -m modules.opportunity_finder.cli run-autopilot` | Reddit + Trends + scout + top 3 + produce |
| `python -m modules.digital_affiliate.cli produce-roundup --auto` | Comparativo 2–3 produtos mesmo nicho |
| `python -m modules.digital_affiliate.cli write-promo --id ID` | Checklists + teaser Reddit |
| `python -m modules.digital_affiliate.cli record-medium-url --id ID --url URL` | Após publicar no Medium |
| `python -m modules.opportunity_finder.cli go-live` | Preflight → select → produce + export |
| `python -m modules.opportunity_finder.cli bootstrap-marketplace` | Cache DS24 + status ClickBank |
| `python -m modules.opportunity_finder.cli scout` | Auto-discover products (DS24 + ClickBank) |
| `python -m modules.opportunity_finder.cli auto-select --top-n 3 --produce` | Top 3 + produce do melhor |
| `python -m modules.digital_affiliate.cli publish --id ID` | Publish review to Medium (API) |
| `python -m modules.opportunity_finder.cli run-week --vertical digital` | Weekly pipeline + export top 3 |
| `python -m modules.digital_affiliate.cli produce --id ID --pins --youtube` | Review + extras promocionais |
| `python -m dashboard` | Streamlit UI — **local** (`http://localhost:8501`) |
| `python -m modules.opportunity_finder.cli fill-pipeline --no-use-ai` | Encher fila até 3 produtos (scout + produce) |
| Dashboard guide | `docs/22-dashboard.md` (local clone) |
| Medium publish guide | `docs/20-medium-manual-publish.md` (local clone) |

Full operations guide: `docs/19-operations.md` (local clone).
| [Medium manual publish](docs/20-medium-manual-publish.md) | Paste `.md` on Medium + sync site |

Full guide (PT): [docs/19-operations.md](docs/19-operations.md) — includes **SiftedBlue** handoff paths.

---

## 🆕 Recent updates (Jul 2026)

### Pipeline digital (infoprodutos)

- **Google Trends** — `enrich-trends` + cap de 10 linhas/run (`config/automation_limits.yaml`)
- **Persona + JTBD** — classificação por subreddit Reddit (`persona_classifier.py`)
- **Pain↔produto** — match explícito Reddit → marketplace (`pain_matcher.py`)
- **Nicho automático** — `niche_classifier` + `keyword_planner` + clusters `roundup` vs `single_review`
- **Top 3** — `auto_select.yaml` → `top_n: 3`; ranking por pain match + score + EPC
- **`run-autopilot`** / **`plan-autopilot`** / **`--dry-run`** — automação com preview seguro
- **Roundup** — `produce-roundup` compara 2–3 produtos do mesmo nicho em 1 matéria
- **Promo** — `write-promo` (checklists Medium/YouTube/Reddit + teaser sem hoplink)
- **Curated multi-vendor** — `config/curated_reviews.yaml` (CB, DS24, vendors nomeados)
- **LLM gateway** — Gemini → Groq → Cerebras → OpenRouter (free tier) + cache
- **Dashboard Streamlit** — `python -m dashboard` ([doc 22](docs/22-dashboard.md))
- **`record-medium-url`** — fecha ciclo após publicação manual no Medium
- **Hoplink Medium** — `tid=medium_<id>` no produce
- **Segurança** — regra Cursor + [doc 19](docs/19-operations.md#-operações-seguras): sem publish automático sem OK

### Infra (anterior)

- **Pipeline unblocked** — marketplace-only scoring (Reddit = dor, não produto)
- **Product scout** — Digistore24 API + ClickBank keyword/gravity
- **`run-week`** — Reddit → Trends → scout → score → export top 3
- **`.env` protected** — nunca commitar secrets

---

## 🔗 Reddit API usage

RE-IA uses the [Reddit Data API](https://www.redditinc.com/policies/data-api-terms) to read **public** subreddit posts for market research (buyer pain, transactional intent).

| Field | Value |
|-------|--------|
| 📄 **About URL** | `https://AndressaLF.github.io/Revenue_Ecosystem-IA/` |
| 🔁 **Redirect URI (dev)** | `http://localhost:8080` |
| 🏷️ **User-Agent** | `RE-IA/0.1 (affiliate research; +https://AndressaLF.github.io/Revenue_Ecosystem-IA/)` |

## 🌐 Live project page

| Where | URL | What you see |
|-------|-----|----------------|
| 📖 **README** (repo home) | [github.com/AndressaLF/Revenue_Ecosystem-IA](https://github.com/AndressaLF/Revenue_Ecosystem-IA) | This document on GitHub |
| 🌍 **GitHub Pages** (site) | [AndressaLF.github.io/Revenue_Ecosystem-IA](https://AndressaLF.github.io/Revenue_Ecosystem-IA/) | Styled landing page (`docs/index.html`) |

👉 **From the README:** click the purple **Live site** badge at the top, or the link in the table above.

**First time?** Enable Pages: repo **Settings → Pages → Branch `main` → Folder `/docs` → Save** — wait 1–3 minutes, then open the Pages URL.

**Optional (off by default):** before a public push, run `python tools/publish_security_check.py` to scan for secrets/PII. To enable on `git push`, see `tools/install_git_hooks.ps1` (`-EnableHook` = warn only; `-Strict` = block).

The **Streamlit dashboard** is not on Pages — start it locally with `python -m dashboard` after `pip install -r requirements.txt`.

---

## 🌍 Who is this for?

- 🧪 Indie builders testing affiliate ideas in **USD markets**
- 📈 People who want **data-backed** product selection, not guesswork
- 🤖 Developers exploring **ethical automation** with human-in-the-loop gates

---

## 📬 Contact & feedback

Questions, ideas, or concerns? Open a **[GitHub Issue](https://github.com/AndressaLF/Revenue_Ecosystem-IA/issues)** — we read every one. 💬

---

## 📜 License & disclaimer

This is a **personal research project**. Not financial advice. Affiliate relationships are disclosed per **FTC guidelines** on any published content.

---

<p align="center">
  <strong>RE-IA</strong> · Revenue Ecosystem IA · Made with curiosity 🚀<br>
  <sub>Last updated · July 2026</sub>
</p>
