# JARVIS-X Windows Installer
Write-Host "Installing JARVIS-X on Windows..." -ForegroundColor Cyan

# Check Python
$pythonVersion = python --version
if (-not $pythonVersion) {
    Write-Host "Python 3.12+ required. Please install from python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
python -m venv jarvis_env
.\jarvis_env\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install Playwright browsers
playwright install chromium firefox webkit

# Setup database
python scripts/setup_database.py

# Create admin user
python scripts/create_admin.py

# Install as Windows service (optional)
# sc.exe create "JARVIS-X" binPath= "C:\path\to\jarvis_env\python.exe backend\main.py"

Write-Host "Installation complete! Run 'python backend/main.py' to start JARVIS-X" -ForegroundColor Green