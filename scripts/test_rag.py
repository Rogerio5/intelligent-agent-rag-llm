import sys
import os

# garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.rag import RAGStore

if __name__ == "__main__":
    rag = RAGStore()
    rag.load_index_from_disk()  # carrega índice salvo em data/index

    while True:
        query = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
        if query.lower() in ["sair", "exit", "quit"]:
            break

        results = rag.retrieve(query, k=3)
        if not results:
            print("⚠️ Nenhum resultado encontrado. Talvez seja preciso rodar load_docs.py primeiro.")
        else:
            print("\n🔎 Resultados:")
            for content, score in results:
                print(f"- {content[:120]}... (score={score:.4f})")
