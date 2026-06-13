# JARVIS-X - Sistema Operativo de IA Personal

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://www.docker.com/)

## Descripción
JARVIS-X es un asistente de inteligencia artificial empresarial que combina múltiples modelos de lenguaje (DeepSeek, OpenAI, Gemini, Claude, Ollama), visión artificial, voz en tiempo real, control total del ordenador y un sistema multiagente autónomo.

## Características Principales
- 🎤 **Voz natural**: Wake word personalizable, STT con Faster Whisper, TTS con ElevenLabs/Fish/Edge, detección de emociones.
- 🧠 **Multi-LLM**: Failover automático entre 5+ proveedores, manteniendo contexto.
- 👁️ **Visión artificial**: OCR, detección de objetos, reconocimiento facial y de emociones, captura de pantalla.
- 🤖 **10 agentes especializados**: Programador, investigador, analista, financiero, marketing, ventas, automatización, seguridad, domótica, StarCars (automotriz).
- 🔌 **MCP completo**: Conectores para GitHub, Telegram, Google Drive, Gmail, Calendar, Notion, Slack, Discord, PostgreSQL, MySQL, MongoDB, Home Assistant, sistema de archivos.
- 💻 **Control total del PC**: Abrir/cerrar aplicaciones, control de ratón/teclado, ejecutar scripts, gestión de ventanas (Windows/Linux/Mac).
- 📦 **Automatización web**: Playwright y Selenium para navegación, scraping y publicación.
- 📱 **Control remoto**: Bot de Telegram, WebSockets en tiempo real.
- 🚗 **Módulo StarCars**: Publicación automática de vehículos en sitio web, Marketplace y redes sociales, generación de financiamiento.
- 💾 **Memoria avanzada**: Corto plazo, largo plazo, episódica y semántica con ChromaDB y RAG.
- 🎨 **Interfaz holográfica**: PyQt6 con efectos visuales inspirados en Iron Man.
- 🔒 **Seguridad**: Cifrado AES-256, roles y permisos, auditoría.

## Requisitos del Sistema
- Python 3.12
- Docker y Docker Compose (opcional para servicios)
- 8 GB RAM mínimo (16 GB recomendado)
- GPU NVIDIA (opcional para aceleración de Whisper)

## Instalación Rápida

### Windows (PowerShell como administrador)
```powershell
git clone https://github.com/tuusuario/JARVIS-X
cd JARVIS-X
.\install_windows.ps1