# ============================================================================
# Script de Push Automatico - AlertaIntruso v4.5.7
# ============================================================================
# Execute: .\push.ps1
# Se der erro de permissão, execute primeiro:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# ============================================================================

Set-Location "d:\#Projetos\AlertaIntruso"

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host " ALERTAINTRUSO v4.5.7 - PUSH PARA GITHUB" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# 0. Validar documentação
Write-Host "[0/7] Validando documentação (README vs CHANGELOG vs Codigo)..." -ForegroundColor Yellow
python validate_documentation.py
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Red
    Write-Host " FALHA NA VALIDACAO DE DOCUMENTACAO!" -ForegroundColor Red
    Write-Host "============================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Corrija os erros acima antes de fazer push" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host ""

# 1. Verificar status
Write-Host "[1/7] Verificando status Git..." -ForegroundColor Yellow
git status
Write-Host ""

# 2. Validar segurança
Write-Host "[2/7] Validando segurança (config.ini deve estar ignorado)..." -ForegroundColor Yellow
$ignored = git check-ignore config.ini
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: config.ini nao esta sendo ignorado!" -ForegroundColor Red
    Write-Host "Verifique .gitignore" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host "[OK] config.ini esta protegido" -ForegroundColor Green
Write-Host ""

# 3. Adicionar arquivos
Write-Host "[3/7] Adicionando arquivos para commit..." -ForegroundColor Yellow
git add -A
Write-Host ""

# 4. Revisar antes de commitar
Write-Host "[4/7] Arquivos a serem commitados:" -ForegroundColor Yellow
git status
Write-Host ""

# 5. Fazer commit
Write-Host "[5/7] Fazendo commit..." -ForegroundColor Yellow
git commit -m "docs: adiciona documentacao de downloads, seguranca e guias v4.5.7

- RESUMO_DOWNLOADS.md: pagina downloads completa
- PAGINA_DOWNLOADS.html: HTML pronto para website
- SUMARIO_EXECUTIVO.md: resumo para decisores
- GUIA_INSTALACAO_DOWNLOAD.md: tutorial passo a passo
- ESPECIFICACAO_TECNICA.json: specs estruturadas
- config.ini.example: template de configuracao seguro
- GUIA_SEGURANCA_REPOSITORIO.md: guia completo seguranca
- CHECKLIST_PRE_PUSH.md: checklist pre-publicacao
- GUIA_GIT_PUSH.md: instrucoes de push
- .gitignore: fortalecido para dados sensiveis
- Verifica e remove dados sensiveis de config.ini"
Write-Host ""

# 6. Fazer push
Write-Host "[6/7] Fazendo push para GitHub..." -ForegroundColor Yellow
git push origin main
Write-Host ""

# 7. Validao final
Write-Host "[7/7] Validacao final..." -ForegroundColor Yellow
Write-Host "[OK] Push concluido!" -ForegroundColor Green
Write-Host ""

# Status final
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host " PUSH CONCLUIDO COM SUCESSO!" -ForegroundColor Green
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Seu repositorio foi atualizado!" -ForegroundColor Green
    Write-Host "Link: https://github.com/Espaco-CMaker/AlertaIntruso" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Red
    Write-Host " ERRO NO PUSH!" -ForegroundColor Red
    Write-Host "============================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Verifique a mensagem de erro acima" -ForegroundColor Yellow
    Write-Host ""
}

Read-Host "Pressione Enter para sair"
