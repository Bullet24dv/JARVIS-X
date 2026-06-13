@echo off
title JARVIS-X Installer for Windows
echo ========================================
echo     JARVIS-X - Windows Installation
echo ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado. Instale Python 3.12 desde python.org
    pause
    exit /b 1
)

:: Crear entorno virtual
echo [1/6] Creando entorno virtual...
python -m venv jarvis_env
call jarvis_env\Scripts\activate.bat

:: Actualizar pip
echo [2/6] Actualizando pip...
python -m pip install --upgrade pip

:: Instalar dependencias
echo [3/6] Instalando dependencias...
pip install -r requirements.txt

:: Instalar PyTorch (CPU)
echo [4/6] Instalando PyTorch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

:: Instalar navegadores Playwright
echo [5/6] Instalando navegadores Playwright...
playwright install chromium firefox webkit

:: Configurar base de datos
echo [6/6] Configurando base de datos...
python scripts/setup_database.py
python scripts/create_admin.py

echo.
echo ========================================
echo    Instalacion completada con exito!
echo    Ejecute: python backend/main.py
echo ========================================
pause