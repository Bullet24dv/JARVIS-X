#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS-X LAUNCHER - Inicia todos los servicios necesarios para el asistente IA.
Uso: python jarvis_launcher.py
"""

import os
import sys
import subprocess
import time
import signal
import threading
import socket
import atexit
from datetime import datetime
from pathlib import Path

# Colores para la consola
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Configuración
PROJECT_ROOT = Path(__file__).parent.absolute()

# Puertos
BACKEND_PORT = 8001

# Procesos en ejecución
processes = []
log_threads = []

def print_header():
    """Imprime cabecera estilizada"""
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}    JARVIS-X LAUNCHER - Asistente IA Empresarial{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")

def log(level, message):
    """Imprime log con timestamp y color"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if level == "INFO":
        color = Colors.GREEN
        prefix = "[INFO]"
    elif level == "WARN":
        color = Colors.YELLOW
        prefix = "[WARN]"
    elif level == "ERROR":
        color = Colors.RED
        prefix = "[ERROR]"
    else:
        color = Colors.RESET
        prefix = "[DEBUG]"
    print(f"{color}{timestamp} {prefix} {message}{Colors.RESET}")

def free_port(port):
    """Intenta liberar el puerto matando el proceso que lo usa (Windows)"""
    if sys.platform == "win32":
        result = subprocess.run(f"netstat -ano | findstr :{port}", shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        pids = set()
        for line in lines:
            if "LISTENING" in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    pids.add(pid)
        for pid in pids:
            try:
                subprocess.run(f"taskkill /PID {pid} /F", shell=True, check=True)
                log("WARN", f"Puerto {port} liberado matando PID {pid}")
            except:
                pass

def start_backend():
    """Inicia el backend con uvicorn y captura logs"""
    log("INFO", "Iniciando backend JARVIS-X...")
    
    # Asegurar que el puerto está libre
    if is_port_in_use(BACKEND_PORT):
        log("WARN", f"Puerto {BACKEND_PORT} ocupado. Intentando liberar...")
        free_port(BACKEND_PORT)
        time.sleep(1)
    
    # Comando para ejecutar uvicorn
    cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", str(BACKEND_PORT), "--reload"]
    
    # Variables de entorno adicionales
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    
    # Iniciar proceso
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
        cwd=str(PROJECT_ROOT)
    )
    processes.append(("backend", process))
    
    # Hilo para leer logs
    def read_logs():
        for line in iter(process.stdout.readline, ''):
            if line:
                # Filtrar mensajes molestos
                if "python-dotenv could not parse" in line:
                    continue
                if "pkg_resources is deprecated" in line:
                    continue
                if "FutureWarning" in line:
                    continue
                print(f"{Colors.BLUE}[BACKEND] {line.rstrip()}{Colors.RESET}")
            else:
                break
    t = threading.Thread(target=read_logs, daemon=True)
    t.start()
    log_threads.append(t)
    return process

def start_frontend():
    """Inicia el frontend (PyQt6) y captura logs"""
    log("INFO", "Iniciando frontend JARVIS-X...")
    cmd = [sys.executable, "-m", "frontend.main"]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
        cwd=str(PROJECT_ROOT)
    )
    processes.append(("frontend", process))
    
    def read_logs():
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"{Colors.MAGENTA}[FRONTEND] {line.rstrip()}{Colors.RESET}")
            else:
                break
    t = threading.Thread(target=read_logs, daemon=True)
    t.start()
    log_threads.append(t)
    return process

def start_frontend_simple():
    """Inicia el frontend simple (alternativa sin WebSocket)"""
    log("INFO", "Iniciando frontend simple JARVIS-X...")
    # Verificar si existe el archivo
    simple_script = PROJECT_ROOT / "frontend_simple.py"
    if not simple_script.exists():
        log("ERROR", "No se encuentra frontend_simple.py")
        return None
    
    cmd = [sys.executable, str(simple_script)]
    env = os.environ.copy()
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
        cwd=str(PROJECT_ROOT)
    )
    processes.append(("frontend_simple", process))
    
    def read_logs():
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"{Colors.MAGENTA}[FRONTEND_SIMPLE] {line.rstrip()}{Colors.RESET}")
            else:
                break
    t = threading.Thread(target=read_logs, daemon=True)
    t.start()
    log_threads.append(t)
    return process

def is_port_in_use(port):
    """Verifica si un puerto está en uso"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def wait_for_backend(timeout=60):
    """Espera a que el backend esté disponible haciendo peticiones a /health"""
    log("INFO", "Esperando a que el backend esté disponible...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            import requests
            resp = requests.get(f"http://127.0.0.1:{BACKEND_PORT}/health", timeout=2)
            if resp.status_code == 200:
                log("INFO", "✅ Backend disponible.")
                return True
        except:
            pass
        time.sleep(2)
    log("WARN", "⚠️ El backend no respondió a tiempo, pero puede estar iniciándose aún.")
    return False

def shutdown():
    """Termina todos los procesos hijos de forma ordenada"""
    log("INFO", "Deteniendo todos los procesos...")
    for name, proc in processes:
        if proc.poll() is None:
            log("INFO", f"Terminando {name} (PID {proc.pid})")
            proc.terminate()
            time.sleep(1)
            if proc.poll() is None:
                proc.kill()
    for t in log_threads:
        t.join(timeout=2)
    log("INFO", "Todos los procesos detenidos.")

def main():
    # Registrar limpieza al salir
    atexit.register(shutdown)
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))

    print_header()
    
    log("INFO", "Usando SQLite como base de datos (sin Docker requerido)")
    
    # Iniciar backend
    backend_proc = start_backend()
    time.sleep(3)
    
    # Esperar a que el backend esté listo
    wait_for_backend()
    
    # Intentar iniciar frontend completo, si falla usar el simple
    frontend_proc = start_frontend()
    
    # Verificar si el frontend completo falló rápidamente
    time.sleep(2)
    if frontend_proc.poll() is not None:
        log("WARN", "El frontend completo no pudo iniciarse. Usando frontend simple...")
        frontend_proc = start_frontend_simple()
    
    log("INFO", "🚀 JARVIS-X completamente iniciado. Presiona Ctrl+C para detener.")
    log("INFO", f"📡 API disponible en: http://127.0.0.1:{BACKEND_PORT}")
    log("INFO", f"📚 Documentación API: http://127.0.0.1:{BACKEND_PORT}/docs")
    
    try:
        while True:
            if backend_proc.poll() is not None:
                log("ERROR", "El backend se detuvo inesperadamente. Saliendo.")
                break
            # Verificar si algún frontend está vivo
            frontend_alive = False
            for name, proc in processes:
                if "frontend" in name and proc.poll() is None:
                    frontend_alive = True
                    break
            if not frontend_alive:
                log("WARN", "No hay frontend activo. Puedes iniciar uno manualmente con 'python frontend_simple.py'")
            time.sleep(2)
    except KeyboardInterrupt:
        log("INFO", "Interrupción recibida. Apagando...")
    finally:
        shutdown()

if __name__ == "__main__":
    main()