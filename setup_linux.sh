#!/bin/bash
set -e

echo "========================================"
echo "     JARVIS-X - Linux Installation"
echo "========================================"

# Verificar Python
if ! command -v python3.12 &> /dev/null; then
    echo "[ERROR] Python 3.12 no encontrado. Instale Python 3.12"
    exit 1
fi

# Instalar dependencias sistema
echo "[1/6] Instalando dependencias del sistema..."
sudo apt update
sudo apt install -y python3.12-venv python3.12-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libsm6 libxext6 libxrender-dev libgomp1 libgl1-mesa-glx tesseract-ocr tesseract-ocr-spa poppler-utils

# Crear entorno virtual
echo "[2/6] Creando entorno virtual..."
python3.12 -m venv jarvis_env
source jarvis_env/bin/activate

# Actualizar pip
echo "[3/6] Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "[4/6] Instalando dependencias Python..."
pip install -r requirements.txt

# Instalar PyTorch CPU
echo "[5/6] Instalando PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Instalar Playwright
echo "[6/6] Instalando navegadores Playwright..."
playwright install chromium firefox webkit
playwright install-deps

# Configurar base de datos
python scripts/setup_database.py
python scripts/create_admin.py

echo ""
echo "========================================"
echo "   Instalacion completada con exito!"
echo "   Ejecute: python backend/main.py"
echo "========================================"