# Instala hooks Git do RE-IA — OPT-IN (desligado por padrão; não bloqueia push).
param(
    [switch]$EnableHook,
    [switch]$Strict
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$hook = Join-Path $Root ".githooks\pre-push"
if (-not (Test-Path $hook)) {
    Write-Error "Hook não encontrado: $hook"
}

if (-not $EnableHook) {
    Write-Host "Auditoria pre-push: DESLIGADA (padrão)."
    Write-Host ""
    Write-Host "Teste manual (não bloqueia nada):"
    Write-Host "  .venv\Scripts\python.exe tools\publish_security_check.py"
    Write-Host ""
    Write-Host "Para ativar no git push (só aviso, push continua):"
    Write-Host "  powershell -File tools\install_git_hooks.ps1 -EnableHook"
    Write-Host ""
    Write-Host "Para bloquear push com falha de segurança:"
    Write-Host "  powershell -File tools\install_git_hooks.ps1 -EnableHook -Strict"
    exit 0
}

git config core.hooksPath .githooks
git config reia.publishSecurityHook true

if ($Strict) {
    git config reia.publishSecurityStrict true
    Write-Host "Hook ativo: modo ESTRITO (push bloqueado se houver secrets/PII)."
} else {
    git config --unset reia.publishSecurityStrict 2>$null
    Write-Host "Hook ativo: modo AVISO (push sempre permitido; só imprime relatório)."
}

Write-Host "core.hooksPath=.githooks"
Write-Host ""
Write-Host "Desativar de novo:"
Write-Host "  git config --unset core.hooksPath"
Write-Host "  git config --unset reia.publishSecurityHook"
