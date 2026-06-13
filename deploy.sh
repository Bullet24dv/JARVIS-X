#!/bin/bash
set -e

echo "=== JARVIS-X Deployment ==="

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "Instalando Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Instalando Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Edita el archivo .env con tus claves API"
    exit 1
fi

# Construir y levantar contenedores
docker-compose build
docker-compose up -d

# Esperar a que la base de datos esté lista
sleep 10

# Ejecutar migraciones
docker-compose exec backend python scripts/setup_database.py

# Crear usuario admin
docker-compose exec backend python scripts/create_admin.py

echo "JARVIS-X desplegado. Accede a http://localhost:8000/docs para la API"
echo "Interfaz gráfica: ejecuta 'python frontend/main.py'"