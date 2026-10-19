"""
Testing RAG Service
"""
from app.rag.rag_service import RAGService


def main():
    """
    Testing RAG Service
    """
    service = RAGService()

    question = "How many casual leaves can an employee take?"
    result = service.query(question)

    print("\n" + "=" * 70)
    print("QUESTION")
    print("=" * 70)
    print(result["question"])

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(result["answer"])

    print("\n" + "=" * 70)
    print("RETRIEVED SOURCES")
    print("=" * 70)

    for source in result["sources"]:
        print(
            f"Distance: {source['distance']:.4f} | "
            f"Section: {source['section']} | "
            f"Page: {source['page_number']}"
        )


if __name__ == "__main__":
    main()
