import asyncio
import sqlite3
import bcrypt
from datetime import datetime
import os

DB_PATH = "jarvis.db"

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

async def main():
    print("📁 Inicializando base de datos SQLite...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            name TEXT,
            email TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    ''')
    
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed = hash_password("jarvis123")
        cursor.execute('''
            INSERT INTO users (username, password, role, name, email, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('admin', hashed, 'admin', 'Administrador', 'admin@jarvis.local', datetime.utcnow(), datetime.utcnow()))
        conn.commit()
        print("✅ Admin creado: admin / jarvis123")
    else:
        print("ℹ️ Admin ya existe")
    
    conn.close()
    print(f"✅ Base de datos: {os.path.abspath(DB_PATH)}")

if __name__ == "__main__":
    asyncio.run(main())