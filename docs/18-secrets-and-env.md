# 🔐 Secrets e Variáveis de Ambiente

> Onde colocar chaves de API com segurança — **nunca** no código nem no Git.

**Arquivo local:** `.env` (criado por você, ignorado pelo Git)  
**Modelo:** [`.env.example`](../.env.example)  
**Código:** `shared_components/config/settings.py`

---

## 📑 Sumário

1. [Como Configurar](#-como-configurar)
2. [Chaves por Prioridade](#-chaves-por-prioridade)
3. [O Que É Obrigatório para Começar](#-o-que-é-obrigatório-para-começar)
4. [Onde Obter Cada Chave](#-onde-obter-cada-chave)
5. [Regras de Segurança](#-regras-de-segurança)
6. [Verificar Configuração](#-verificar-configuração)

---

## ⚙️ Como Configurar

```bash
# Na raiz do projeto
copy .env.example .env    # Windows
# cp .env.example .env    # Linux/macOS

# Edite .env com um editor de texto — preencha só o que for usar agora
```

| Arquivo | Commitar no Git? | Função |
|---------|------------------|--------|
| `.env.example` | ✅ Sim | Modelo sem valores reais |
| `.env` | ❌ **Nunca** | Suas chaves reais |
| `config/product_seed.yaml` | ⚠️ Cuidado | Hoplinks — preferir `.env` + seed sem secrets |
| `storage/` | ❌ Não | Banco SQLite local |

---

## 🔑 Chaves por Prioridade

### P0 — Para implementar automação + IA (semana 9–15)

| Variável | Obrigatória? | Uso |
|----------|--------------|-----|
| `GEMINI_API_KEY` | **Sim** (produce automático, desempate IA) | `gemini_client`, artigos, pin titles |

Sem Gemini: ingest + score + auto-select por regras funcionam; **produce com IA não**.

### P1 — Afiliados (não são senhas secretas)

| Variável | Obrigatória? | Uso |
|----------|--------------|-----|
| `CLICKBANK_NICKNAME` | Recomendado | Montar hoplinks no `produce` |
| `DIGISTORE24_AFFILIATE_ID` | Recomendado | Hoplinks DS24 |
| `AMAZON_ASSOCIATE_TAG` | Só se físico | Links Amazon |

Alternativa: hoplinks **completos** em `config/product_seed.yaml` (sem precisar dessas vars).

### P2 — Scout automático de produtos (opcional)

| Variável | Plataforma | Uso |
|----------|------------|-----|
| `DIGISTORE24_API_KEY` | Digistore24 | Scout catálogo + comissões (readonly) — **afiliado pode** |

### Digistore24 — afiliado pode ter API key?

**Sim.** Conta ativa de afiliado pode gerar API key **sem aprovação extra**. A tela fica em *Settings → Account access → API keys* (às vezes rotulada “vendor view”, mas funciona para afiliados).

| Permissão | Afiliado precisa? | Uso no RE-IA |
|-----------|-------------------|--------------|
| **Read access** (readonly) | ✅ **Sim — use esta** | Listar produtos, vendas/comissões, relatórios |
| **Full access** (writable) | ❌ Não | Cancelar pedidos etc. — desnecessário |
| **Developer** | ❌ Não | Só para apps que geram keys para outros usuários |
| **Shipping service provider** | ❌ Não | Logística de vendedor |

**Como criar:**

1. Login em [digistore24.com](https://www.digistore24.com)
2. **Settings** → **Account access** → aba **API keys** → **New API key**
   - Ou portal: [dev.digistore24.com](https://dev.digistore24.com/) → Create API key
3. Nome: `re-ia-readonly`
4. Permissão: **Read access** apenas
5. Copie a key → `.env`:

```env
DIGISTORE24_API_KEY=sua-chave-aqui
DIGISTORE24_AFFILIATE_ID=seu_id_afiliado
```

**Header HTTP:** `X-DS-API-KEY: <sua-chave>`

**O que a API faz para afiliado:** consultar produtos (`listProducts`), vendas e dados da conta — útil para `scout-digistore24` automático. **Não** substitui hoplink no marketplace; o ID de afiliado continua em `DIGISTORE24_AFFILIATE_ID` para links.

| `CLICKBANK_API_KEY` | ClickBank | Métricas afiliado (Analytics API) — **não** Products API |

Sem API marketplace: use **`config/product_seed.yaml`** (seed manual 1×) + **`auto-select`** automático.

### P2 — Reddit OAuth (opcional)

| Variável | Uso |
|----------|-----|
| `REDDIT_CLIENT_ID` | Rate limit maior |
| `REDDIT_CLIENT_SECRET` | OAuth |

**MVP funciona sem** — ingest via `reddit.com/.../.json` público.

### P3 — Publicação semi-automática (opcional)

| Variável | Uso |
|----------|-----|
| `MEDIUM_INTEGRATION_TOKEN` | Rascunho automático no Medium |
| `PINTEREST_ACCESS_TOKEN` | Pins via API (futuro) |

### P3 — Outros

| Variável | Uso |
|----------|-----|
| `PRODUCTHUNT_TOKEN` | Ingest SaaS (módulo 02) |

### Nomad

**Não usa variável no `.env`** — recebimento é configurado no app Nomad + painéis afiliados (PayPal/banco).

---

## ✅ O Que É Obrigatório para Começar

### Mínimo para eu (Cursor) programar o pacote P0 esta semana

```
GEMINI_API_KEY=          ← única secret obrigatória para IA
```

+ uma vez: `config/product_seed.yaml` com 5–10 produtos CB/DS24 (hoplinks seus)

### Mínimo para **você** rodar a 1ª semana automatizada

```
GEMINI_API_KEY=
CLICKBANK_NICKNAME=      (ou hoplinks completos no seed)
DIGISTORE24_AFFILIATE_ID=
```

### Não precisa agora

- Reddit OAuth  
- Amazon tag (se foco digital)  
- Medium / Pinterest tokens  
- ClickBank / Digistore24 API keys (até implementarmos scout)  
- Product Hunt  

---

## 📍 Onde Obter Cada Chave

| Chave | Onde obter |
|-------|------------|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) — gratuito com cota |
| `REDDIT_CLIENT_ID/SECRET` | [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) → tipo "script" |
| `DIGISTORE24_API_KEY` | Digistore24 App → Configurações → API |
### ClickBank — qual API / chave marcar?

Você é **afiliado**, não vendedor (vendor). Na tela **Settings → API Management → Create API Key**:

| Permissão na ClickBank | Afiliado precisa? | Uso no RE-IA |
|------------------------|-------------------|--------------|
| **Analytics API** | ✅ **Sim** (esta é a principal) | Vendas, cliques, EPC, pivot automático, dashboard |
| **Products API** | ❌ **Não** | Só para **vendedores** gerenciarem produtos próprios — **não lista o marketplace** |
| **Orders / Tickets API** | ❌ Não no MVP | Suporte a pedidos — irrelevante para escolher produto |
| **Developer API Key** | ❌ Obsoleta | Não criar; integrações novas não usam |

**O que colocar no `.env`:**

```env
CLICKBANK_API_KEY=API-xxxxxxxx...    # UMA chave com permissão Analytics
CLICKBANK_NICKNAME=seu_nickname       # Para hoplinks (não é secret)
```

**Como criar (conta primária / master):**

1. Settings → **API Management** → **Create New API Key**
2. Nome: `re-ia-analytics`
3. Marque **Analytics API** para o seu **nickname** de afiliado
4. **Não** marque Products API (você não é seller)
5. Save → copie a chave `API-...` para `CLICKBANK_API_KEY`

**Importante:** a API **não substitui** o marketplace para **descobrir** produtos novos. Ela serve para **medir** o que já promove. Para escolha automática de produto usamos `config/product_seed.yaml` + `auto-select` (dor Reddit × seed).

Se a interface mostrar siglas extras (ex. integrações antigas tipo “Clerk” / “APO”), ignore — use o modelo atual: **uma API Key com Analytics** em [API Management](https://support.clickbank.com/en/articles/10535395-how-to-create-clickbank-api-keys).

| `CLICKBANK_NICKNAME` | ClickBank → Account → Nickname |
| `DIGISTORE24_AFFILIATE_ID` | Painel afiliado Digistore24 |
| `AMAZON_ASSOCIATE_TAG` | Amazon Associates → Tracking ID |
| `MEDIUM_INTEGRATION_TOKEN` | Medium → Settings → Security → Integration tokens |
| `PINTEREST_ACCESS_TOKEN` | [developers.pinterest.com](https://developers.pinterest.com/) |

---

## 🛡️ Regras de Segurança

1. **`.env` nunca no Git** — já está em `.gitignore`
2. **Não colar chaves no chat** — use placeholders ao pedir ajuda
3. **Não hardcodar** em `.py` — sempre `get_settings()` ou `os.getenv`
4. **`SecretStr`** no Pydantic — evita log acidental
5. **Rotação:** se vazar, revogue no painel e gere nova
6. **CI futuro:** GitHub Actions → **Secrets** do repositório, não `.env` no repo
7. **`product_seed.yaml`:** se tiver hoplinks com tokens, adicione ao `.gitignore` ou use variáveis

### Arquivos ignorados pelo Git

```
.env
.env.local
.env.*          (exceto .env.example)
secrets/
storage/
```

---

## 🧪 Verificar Configuração

```bash
.venv\Scripts\activate
python -m shared_components.config.check_env
```

Saída esperada: lista do que está configurado (sem mostrar valores completos das secrets).

---

*Última atualização: julho/2026*
