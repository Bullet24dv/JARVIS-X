# ============================================================
# JARVIS-X | backend/core/memory/manager.py
# Sistema de memoria: corto/largo plazo, episódica, semántica, RAG
# ============================================================

import asyncio
import json
import logging
import uuid
from collections import deque
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import chromadb
from chromadb.config import Settings as ChromaSettings

from backend.config import settings

logger = logging.getLogger("jarvis.memory")


class ConversationTurn:
    def __init__(self, role: str, content: str, metadata: Optional[Dict] = None):
        self.id = str(uuid.uuid4())
        self.role = role
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


class MemoryManager:
    """
    Gestor de memoria de JARVIS-X:
    - Memoria de corto plazo: deque en RAM (últimas N conversaciones)
    - Memoria de largo plazo: ChromaDB con búsqueda semántica
    - Memoria episódica: eventos específicos con timestamp
    - Memoria semántica: hechos y conocimiento general
    - RAG: recuperación aumentada de contexto
    """

    def __init__(self):
        self._short_term: deque[ConversationTurn] = deque(maxlen=settings.SHORT_TERM_MEMORY_SIZE)
        self._chroma_client: Optional[chromadb.AsyncHttpClient] = None
        self._collection_memory: Optional[Any] = None
        self._collection_docs: Optional[Any] = None
        self._collection_episodes: Optional[Any] = None
        self._embedding_fn: Optional[Any] = None
        self._initialized = False

    async def initialize(self):
        """Conecta con ChromaDB e inicializa colecciones."""
        try:
            # Intenta conectar a ChromaDB remoto primero
            self._chroma_client = chromadb.AsyncHttpClient(
                host=settings.CHROMA_HOST,
                port=settings.CHROMA_PORT,
            )
            await self._chroma_client.heartbeat()
            logger.info("ChromaDB conectado (modo servidor)")
        except Exception:
            # Fallback: ChromaDB local persistente
            logger.warning("ChromaDB remoto no disponible. Usando modo local persistente.")
            import chromadb
            self._chroma_client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=ChromaSettings(anonymized_telemetry=False),
            )

        # Función de embedding
        try:
            from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
            if settings.OPENAI_API_KEY:
                self._embedding_fn = OpenAIEmbeddingFunction(
                    api_key=settings.OPENAI_API_KEY,
                    model_name=settings.EMBEDDING_MODEL,
                )
        except Exception:
            pass

        if not self._embedding_fn:
            try:
                from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
                self._embedding_fn = SentenceTransformerEmbeddingFunction(
                    model_name="paraphrase-multilingual-MiniLM-L12-v2"
                )
                logger.info("Usando SentenceTransformer para embeddings (local)")
            except Exception as e:
                logger.warning(f"Sin función de embedding disponible: {e}")

        # Crear / obtener colecciones
        get_or_create = (
            self._chroma_client.get_or_create_collection
            if hasattr(self._chroma_client, "get_or_create_collection")
            else self._chroma_client.get_or_create_collection
        )

        kwargs = {"embedding_function": self._embedding_fn} if self._embedding_fn else {}

        self._collection_memory = await self._async_get_or_create(
            settings.CHROMA_COLLECTION_MEMORY, **kwargs
        )
        self._collection_docs = await self._async_get_or_create(
            settings.CHROMA_COLLECTION_DOCS, **kwargs
        )
        self._collection_episodes = await self._async_get_or_create(
            "jarvis_episodes", **kwargs
        )

        self._initialized = True
        logger.info("Sistema de memoria inicializado correctamente")

    async def _async_get_or_create(self, name: str, **kwargs):
        """Crea o recupera colección ChromaDB (sync/async compatible)."""
        try:
            if asyncio.iscoroutinefunction(self._chroma_client.get_or_create_collection):
                return await self._chroma_client.get_or_create_collection(name=name, **kwargs)
            else:
                return await asyncio.to_thread(
                    self._chroma_client.get_or_create_collection, name=name, **kwargs
                )
        except Exception as e:
            logger.error(f"Error creando colección '{name}': {e}")
            return None

    # ── Memoria de corto plazo ────────────────────────────────
    def add_turn(self, role: str, content: str, metadata: Optional[Dict] = None) -> ConversationTurn:
        """Agrega un turno a la memoria de corto plazo."""
        turn = ConversationTurn(role=role, content=content, metadata=metadata)
        self._short_term.append(turn)
        return turn

    def get_short_term(self, last_n: Optional[int] = None) -> List[Dict]:
        """Retorna los últimos N turnos de la conversación."""
        turns = list(self._short_term)
        if last_n:
            turns = turns[-last_n:]
        return [t.to_dict() for t in turns]

    def get_short_term_as_messages(self, last_n: Optional[int] = None) -> List[Dict[str, str]]:
        """Retorna turnos en formato messages para LLM."""
        turns = list(self._short_term)
        if last_n:
            turns = turns[-last_n:]
        return [{"role": t.role, "content": t.content} for t in turns]

    def clear_short_term(self):
        """Limpia la memoria de corto plazo."""
        self._short_term.clear()

    # ── Memoria de largo plazo ────────────────────────────────
    async def save_to_long_term(
        self,
        content: str,
        memory_type: str = "conversation",
        metadata: Optional[Dict] = None,
    ) -> str:
        """Guarda contenido en memoria de largo plazo (ChromaDB)."""
        if not self._collection_memory:
            logger.warning("Memoria de largo plazo no disponible")
            return ""

        mem_id = str(uuid.uuid4())
        meta = {
            "type": memory_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **(metadata or {}),
        }

        try:
            await asyncio.to_thread(
                self._collection_memory.add,
                ids=[mem_id],
                documents=[content],
                metadatas=[meta],
            )
            return mem_id
        except Exception as e:
            logger.error(f"Error guardando en memoria larga: {e}")
            return ""

    async def search_memory(
        self,
        query: str,
        top_k: int = None,
        memory_type: Optional[str] = None,
        threshold: float = None,
    ) -> List[Dict]:
        """Búsqueda semántica en memoria de largo plazo (RAG)."""
        if not self._collection_memory:
            return []

        top_k = top_k or settings.RAG_TOP_K
        threshold = threshold or settings.RAG_THRESHOLD

        where = {"type": memory_type} if memory_type else None

        try:
            kwargs = {
                "query_texts": [query],
                "n_results": top_k,
            }
            if where:
                kwargs["where"] = where

            results = await asyncio.to_thread(
                self._collection_memory.query, **kwargs
            )

            memories = []
            if results and results.get("documents"):
                docs = results["documents"][0]
                metas = results.get("metadatas", [[]])[0]
                distances = results.get("distances", [[]])[0]

                for doc, meta, dist in zip(docs, metas, distances):
                    similarity = 1 - dist  # ChromaDB usa distancia coseno
                    if similarity >= threshold:
                        memories.append({
                            "content": doc,
                            "metadata": meta,
                            "similarity": round(similarity, 4),
                        })

            return sorted(memories, key=lambda x: x["similarity"], reverse=True)

        except Exception as e:
            logger.error(f"Error en búsqueda semántica: {e}")
            return []

    # ── Memoria episódica ────────────────────────────────────
    async def save_episode(
        self,
        event: str,
        details: str,
        agent: Optional[str] = None,
    ) -> str:
        """Guarda un evento episódico (acción realizada, resultado, etc.)."""
        if not self._collection_episodes:
            return ""

        ep_id = str(uuid.uuid4())
        content = f"[EVENTO] {event}\n[DETALLES] {details}"
        meta = {
            "type": "episode",
            "event": event,
            "agent": agent or "jarvis",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        try:
            await asyncio.to_thread(
                self._collection_episodes.add,
                ids=[ep_id],
                documents=[content],
                metadatas=[meta],
            )
            return ep_id
        except Exception as e:
            logger.error(f"Error guardando episodio: {e}")
            return ""

    # ── Documentos (RAG) ─────────────────────────────────────
    async def index_document(
        self,
        content: str,
        source: str,
        doc_type: str = "text",
        chunk_size: int = 1000,
        overlap: int = 200,
    ) -> List[str]:
        """Indexa un documento dividiéndolo en chunks para RAG."""
        if not self._collection_docs:
            return []

        # Chunking simple con overlap
        chunks = []
        for i in range(0, len(content), chunk_size - overlap):
            chunk = content[i: i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)

        ids = [str(uuid.uuid4()) for _ in chunks]
        metas = [
            {
                "source": source,
                "type": doc_type,
                "chunk_index": idx,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            for idx, _ in enumerate(chunks)
        ]

        try:
            await asyncio.to_thread(
                self._collection_docs.add,
                ids=ids,
                documents=chunks,
                metadatas=metas,
            )
            logger.info(f"Documento '{source}' indexado en {len(chunks)} chunks")
            return ids
        except Exception as e:
            logger.error(f"Error indexando documento: {e}")
            return []

    async def search_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        """Busca en documentos indexados."""
        if not self._collection_docs:
            return []
        try:
            results = await asyncio.to_thread(
                self._collection_docs.query,
                query_texts=[query],
                n_results=top_k,
            )
            docs = []
            if results and results.get("documents"):
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results.get("metadatas", [[]])[0],
                    results.get("distances", [[]])[0],
                ):
                    docs.append({"content": doc, "metadata": meta, "similarity": round(1 - dist, 4)})
            return docs
        except Exception as e:
            logger.error(f"Error buscando documentos: {e}")
            return []

    # ── Contexto enriquecido para LLM ────────────────────────
    async def get_enriched_context(self, query: str) -> str:
        """
        Construye contexto enriquecido combinando:
        - Memoria de corto plazo reciente
        - Recuerdos relevantes de largo plazo
        - Documentos relevantes
        """
        sections = []

        # Historial reciente
        recent = self.get_short_term(last_n=10)
        if recent:
            history = "\n".join(
                f"{t['role'].upper()}: {t['content'][:200]}" for t in recent[-6:]
            )
            sections.append(f"[CONVERSACIÓN RECIENTE]\n{history}")

        # Búsqueda en memoria larga
        memories = await self.search_memory(query, top_k=3)
        if memories:
            mem_text = "\n".join(f"- {m['content'][:300]}" for m in memories)
            sections.append(f"[RECUERDOS RELEVANTES]\n{mem_text}")

        # Búsqueda en documentos
        docs = await self.search_documents(query, top_k=3)
        if docs:
            doc_text = "\n".join(
                f"- [{d['metadata'].get('source', 'doc')}] {d['content'][:400]}" for d in docs
            )
            sections.append(f"[DOCUMENTOS RELEVANTES]\n{doc_text}")

        return "\n\n".join(sections) if sections else ""

    async def get_stats(self) -> Dict[str, Any]:
        """Estadísticas del sistema de memoria."""
        stats: Dict[str, Any] = {
            "short_term_turns": len(self._short_term),
            "initialized": self._initialized,
        }
        for name, col in [
            ("long_term", self._collection_memory),
            ("documents", self._collection_docs),
            ("episodes", self._collection_episodes),
        ]:
            if col:
                try:
                    count = await asyncio.to_thread(col.count)
                    stats[f"{name}_count"] = count
                except Exception:
                    stats[f"{name}_count"] = "?"
        return stats