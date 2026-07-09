# Publicar GitHub Pages (RE-IA)

Página do projeto para cadastro da **Reddit API**: `docs/index.html`

## 1. Criar repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Nome sugerido: **`re-ia`**
3. Visibilidade: **Public** (Pages gratuito)
4. **Não** marque README inicial se já tiver código local
5. Create repository

## 2. Enviar código (primeira vez)

Na pasta do projeto:

```powershell
cd "y:\repositorios_github\como_minerar\New folder"

git remote add origin https://github.com/SEU_USUARIO/re-ia.git
git branch -M main
git push -u origin main
```

Substitua `SEU_USUARIO` pelo seu login GitHub.

## 3. Ativar GitHub Pages

1. Repositório → **Settings** → **Pages**
2. **Build and deployment** → Source: **Deploy from a branch**
3. Branch: **`main`** → Folder: **`/docs`**
4. Save

Em 1–3 minutos a URL ficará:

```text
https://SEU_USUARIO.github.io/re-ia/
```

## 4. Atualizar links na página

Edite `docs/index.html` e troque `YOUR_USERNAME` pelo seu usuário GitHub (User-Agent e link do repo).

Commit e push de novo.

## 5. Cadastrar app Reddit

1. [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) → **create another app**
2. Tipo: **web app** (ou **script** para uso só local)
3. **name:** `RE-IA Research`
4. **redirect uri:** `http://localhost:8080`
5. **about url:** `https://SEU_USUARIO.github.io/re-ia/`
6. Copie **client id** e **secret** → `.env`:

```env
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
```

## Checklist

- [ ] Repositório público criado
- [ ] Push feito
- [ ] Pages ativo em `/docs`
- [ ] URL abre no navegador
- [ ] `index.html` com seu username
- [ ] Reddit app criado com about URL da Pages
