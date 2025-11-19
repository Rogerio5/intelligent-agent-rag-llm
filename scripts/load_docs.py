import os
from core.rag import RAGStore

def load_documents_from_folder(folder="data/docs"):
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs

if __name__ == "__main__":
    rag = RAGStore()
    documents = load_documents_from_folder()
    rag.build_or_load_index(documents)
    rag.save_index()
    print("✅ Índice RAG atualizado com documentos de FAQ.")
