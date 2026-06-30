@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo   INSTALADOR DE DEPENDENCIAS - Looqbox Cases
echo ============================================================
echo.

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python nao encontrado no PATH do computador.
    echo Instale o Python e marque a opcao "Add Python to PATH".
    pause
    exit /b 1
)

if not exist "%~dp0requirements.txt" (
    echo [ERRO] Arquivo requirements.txt nao encontrado nesta pasta.
    pause
    exit /b 1
)

echo Atualizando o pip...
python -m pip install --upgrade pip

echo.
echo Instalando bibliotecas do requirements.txt...
echo.
python -m pip install -r "%~dp0requirements.txt"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao instalar as dependencias.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   CONCLUIDO
echo ============================================================
echo.
echo Bibliotecas instaladas a partir do requirements.txt:
echo   - PyMySQL          (conexao com o banco MySQL)
echo   - python-dotenv    (leitura das variaveis do arquivo .env)
echo.
pause
