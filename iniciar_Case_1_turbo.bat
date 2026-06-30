@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo   Consulta de Vendas Iniciado...
echo ============================================================

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python nao encontrado no PATH do computador.
    echo Instale o Python e marque a opcao "Add Python to PATH".
    pause
    exit /b 1
)

python "%~dp0Case_1.py"
pause
