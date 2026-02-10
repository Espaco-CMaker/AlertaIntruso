@echo off
REM ============================================================================
REM Script de Push Automatico - AlertaIntruso v4.5.7
REM ============================================================================
REM Este script faz o commit e push automaticamente
REM Apenas execute: python_push.bat (ou: push.bat no PowerShell)
REM ============================================================================

cd /d d:\#Projetos\AlertaIntruso

echo.
echo ============================================================================
echo  ALERTAINTRUSO v4.5.7 - PUSH PARA GITHUB
echo ============================================================================
echo.

REM Verificar status
echo [1/6] Verificando status Git...
git status
echo.

REM Confirmar que config.ini está ignorado
echo [2/6] Validando segurança (config.ini deve estar ignorado)...
git check-ignore config.ini
if errorlevel 1 (
    echo AVISO: config.ini nao esta sendo ignorado!
    pause
    exit /b 1
)
echo [OK] config.ini esta protegido
echo.

REM Adicionar arquivos
echo [3/6] Adicionando arquivos para commit...
git add -A
echo.

REM Revisar antes de commitar
echo [4/6] Arquivos a serem commitados:
git status
echo.

REM Fazer commit
echo [5/6] Fazendo commit...
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "docs: atualiza README e changelog"
) else (
    echo Nenhuma mudanca para commitar.
)
echo.

REM Fazer push
echo [6/6] Fazendo push para GitHub...
git push origin main
echo.

REM Status final
echo.
echo ============================================================================
echo  PUSH CONCLUIDO COM SUCESSO!
echo ============================================================================
echo.
echo Seu repositorio foi atualizado!
echo Link: https://github.com/Espaco-CMaker/AlertaIntruso
echo.
pause
