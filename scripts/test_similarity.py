from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.ingestion.pdf_loader import extract_pages
from app.ingestion.chunker import chunk_pages

PDF_PATH = "data/acme-simple_employee_leave_policy.pdf"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def main():
    # Load document
    pages = extract_pages(PDF_PATH)

    # Create logical chunks
    chunks = chunk_pages(pages)

    # For now, exclude evaluation data (section 7)
    knowledge_chunks = chunks[:6]

    # Load embedding model
    model = SentenceTransformer(MODEL_NAME)

    # User question
    query = "How many casual leaves can an employee take?"

    # Embed query
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    results = []

    # Compare query against every knowledge chunk
    for chunk in knowledge_chunks:

        chunk_embedding = model.encode(
            chunk["text"],
            normalize_embeddings=True
        )

        score = cosine_similarity(
            [query_embedding],
            [chunk_embedding]
        )[0][0]

        results.append({
            "section": chunk["section"],
            "score": score
        })

    # Highest similarity first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    print("Query:")
    print(query)

    print("\nSimilarity results:")
    print("-" * 60)

    for result in results:
        print(
            f"{result['score']:.4f} | "
            f"{result['section']}"
        )


if __name__ == "__main__":
    main()