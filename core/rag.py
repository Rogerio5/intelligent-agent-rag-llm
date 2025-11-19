import os
import logging
from typing import List, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DEFAULT_INDEX_DIR = os.getenv("INDEX_DIR", "data/index")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

class RAGStore:
    def __init__(self):
        try:
            logger.info(f"Carregando embeddings com modelo {EMBED_MODEL}...")
            self.embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
            self.vectorstore = None
        except Exception as e:
            logger.error(f"Erro ao inicializar embeddings: {e}")
            self.embeddings, self.vectorstore = None, None

    def build_or_load_index(self, documents: List[str]) -> None:
        if not self.embeddings:
            logger.warning("Embeddings não inicializados.")
            return

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = []
        for doc in documents:
            chunks.extend(splitter.split_text(doc))

        logger.info(f"Construindo índice FAISS com {len(chunks)} chunks...")
        self.vectorstore = FAISS.from_texts(chunks, self.embeddings)

    def load_index_from_disk(self, path: str = DEFAULT_INDEX_DIR) -> None:
        if not self.embeddings:
            logger.warning("Embeddings não inicializados.")
            return

        if os.path.exists(path):
            try:
                logger.info(f"Carregando índice FAISS de {path}...")
                self.vectorstore = FAISS.load_local(
                    path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Índice carregado com sucesso.")
            except Exception as e:
                logger.error(f"Erro ao carregar índice: {e}")
        else:
            logger.warning(f"Nenhum índice encontrado em {path}.")

    def save_index(self, path: str = DEFAULT_INDEX_DIR) -> None:
        if self.vectorstore:
            try:
                os.makedirs(path, exist_ok=True)
                self.vectorstore.save_local(path)
                logger.info(f"Índice salvo em {path}.")
            except Exception as e:
                logger.error(f"Erro ao salvar índice: {e}")

    def retrieve(self, query: str, k: int = 4) -> List[Tuple[str, float]]:
        if not self.vectorstore:
            logger.warning("Nenhum índice carregado para busca.")
            return []
        try:
            docs = self.vectorstore.similarity_search_with_score(query, k=k)
            return [(d.page_content, score) for d, score in docs]
        except Exception as e:
            logger.error(f"Erro na recuperação de contexto: {e}")
            return []
