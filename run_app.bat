@echo off
chcp 65001 >nul
title CarreiraIA 2030 - Ferramenta de Carreira Inteligente

echo ===================================================================
echo             CarreiraIA 2030 - Inicializador do Sistema
echo ===================================================================
echo.

set PY_CMD=

python --version >nul 2>&1
if not errorlevel 1 (
    set PY_CMD=python
    goto RUN
)

py --version >nul 2>&1
if not errorlevel 1 (
    set PY_CMD=py
    goto RUN
)

echo [AVISO] O Python nao foi encontrado no PATH do Windows.
echo.
echo Tentando caminhos comuns de instalacao...
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PY_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto RUN
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PY_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto RUN
)
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set PY_CMD="%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    goto RUN
)

echo.
echo Por favor, instale o Python em https://www.python.org/downloads/
echo e lembre-se de marcar "Add Python to PATH".
echo.
pause
exit /b

:RUN
echo [OK] Usando interpretador Python: %PY_CMD%
echo.
echo [1/2] Verificando dependencias...
%PY_CMD% -m pip install -r requirements.txt
echo.
echo [2/2] Iniciando aplicacao Streamlit...
echo Se o navegador nao abrir sozinho, acesse: http://localhost:8501
echo.
%PY_CMD% -m streamlit run app.py --server.headless false --browser.gatherUsageStats false
if errorlevel 1 (
    echo.
    echo Ocorreu uma interrupcao no Streamlit.
    pause
)
