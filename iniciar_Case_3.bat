@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo   Case 3 - Graficos lado a lado iniciado...
echo ============================================================

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python nao encontrado no PATH do computador.
    echo Instale o Python e marque a opcao "Add Python to PATH".
    pause
    exit /b 1
)

python "%~dp0Case_3_graficos_lado_a_lado.py"
echo.
echo Saida gerada em: analise_imdb\charts\case3_graficos_lado_a_lado.png
pause
