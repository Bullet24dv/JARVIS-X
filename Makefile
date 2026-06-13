.PHONY: help install dev build up down logs clean test

help:
	@echo "Comandos disponibles:"
	@echo "  install      Instalar dependencias"
	@echo "  dev          Ejecutar en modo desarrollo"
	@echo "  build        Construir imágenes Docker"
	@echo "  up           Levantar contenedores"
	@echo "  down         Detener contenedores"
	@echo "  logs         Ver logs"
	@echo "  clean        Limpiar archivos temporales"
	@echo "  test         Ejecutar pruebas"

install:
	pip install -r requirements.txt
	playwright install chromium firefox webkit

dev:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage

test:
	pytest tests/ -v --cov=backend --cov-report=term