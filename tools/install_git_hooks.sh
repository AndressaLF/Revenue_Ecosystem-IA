#!/usr/bin/env bash
# Instala hooks Git do RE-IA — OPT-IN (desligado por padrão; não bloqueia push).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ENABLE_HOOK=false
STRICT=false
for arg in "$@"; do
  case "$arg" in
    --enable-hook) ENABLE_HOOK=true ;;
    --strict) STRICT=true ;;
    -h|--help)
      echo "Uso: bash tools/install_git_hooks.sh [--enable-hook] [--strict]"
      exit 0
      ;;
  esac
done

if [[ ! -f "$ROOT/.githooks/pre-push" ]]; then
  echo "Hook não encontrado: $ROOT/.githooks/pre-push" >&2
  exit 1
fi

if [[ "$ENABLE_HOOK" != "true" ]]; then
  echo "Auditoria pre-push: DESLIGADA (padrão)."
  echo ""
  echo "Teste manual (não bloqueia nada):"
  echo "  .venv/Scripts/python.exe tools/publish_security_check.py"
  echo ""
  echo "Para ativar no git push (só aviso):"
  echo "  bash tools/install_git_hooks.sh --enable-hook"
  echo ""
  echo "Para bloquear push com falha:"
  echo "  bash tools/install_git_hooks.sh --enable-hook --strict"
  exit 0
fi

git config core.hooksPath .githooks
git config reia.publishSecurityHook true
chmod +x .githooks/pre-push 2>/dev/null || true

if [[ "$STRICT" == "true" ]]; then
  git config reia.publishSecurityStrict true
  echo "Hook ativo: modo ESTRITO (push bloqueado se houver secrets/PII)."
else
  git config --unset reia.publishSecurityStrict 2>/dev/null || true
  echo "Hook ativo: modo AVISO (push sempre permitido)."
fi

echo "core.hooksPath=.githooks"
