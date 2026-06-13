# ============================================================
# JARVIS-X | backend/core/database.py
# SQLAlchemy 2.0 async con PostgreSQL + SQLite fallback
# ============================================================

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from backend.config import settings

logger = logging.getLogger("jarvis.database")


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos ORM."""
    pass


# ── Motor PostgreSQL (primario) ───────────────────────────────
try:
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
    _using_postgres = True
except Exception:
    # Fallback SQLite
    logger.warning("PostgreSQL no disponible. Usando SQLite local.")
    engine = create_async_engine(
        settings.SQLITE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},
    )
    _using_postgres = False


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def init_db():
    """Crea las tablas si no existen."""
    # Importar modelos para que se registren en Base.metadata
    from backend.models import user, conversation, task, memory  # noqa: F401

    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Base de datos inicializada correctamente")
        except Exception as e:
            logger.error(f"Error inicializando base de datos: {e}")
            raise


async def close_db():
    """Cierra el motor de base de datos."""
    await engine.dispose()
    logger.info("Conexión a base de datos cerrada")


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Context manager para sesiones de base de datos."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia FastAPI para inyección de sesión de BD."""
    async with get_db_session() as session:
        yield session