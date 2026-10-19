from app.ingestion.embedder import Embedder
from app.storage.vector_store import search_similar

def main():
    query = "How many casual leaves can an employee take?"

    # Convert the question into the same 384-dimensional
    # embedding space as our document chunks.
    embedder = Embedder()

    query_embedding = embedder.embed(query)

    print("Query:")
    print(query)

    print("\nQuery embedding dimensions:")
    print(len(query_embedding))

    # Ask PostgreSQL + pgvector for the most similar chunks.
    results = search_similar(
        query_embedding=query_embedding,
        top_k=3,
    )

    print("\nTop results:")
    print("-" * 70)

    for result in results:
        print(
            f"Distance: {result['distance']:.4f} | "
            f"{result['section']}"
        )


if __name__ == "__main__":
    main()