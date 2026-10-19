from app.ingestion.embedder import Embedder
from app.storage.vector_store import search_similar
from app.rag.context_builder import build_context


def main():

    query = "How many casual leaves can an employee take?"

    # 1. Embed query
    embedder = Embedder()
    query_embedding = embedder.embed(query)

    # 2. Retrieve Top-K chunks
    results = search_similar(
        query_embedding=query_embedding,
        top_k=3,
    )

    # 3. Build LLM context
    context = build_context(results)

    print("USER QUESTION")
    print("-" * 70)
    print(query)

    print("\nRETRIEVED CONTEXT")
    print("-" * 70)
    print(context)


if __name__ == "__main__":
    main()