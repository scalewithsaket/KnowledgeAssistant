from app.ingestion.embedder import Embedder
from app.storage.vector_store import search_similar
from app.rag.context_builder import build_context
from app.rag.prompt_builder import SYSTEM_PROMPT, build_user_prompt


def main():

    query = "How many casual leaves can an employee take?"

    # 1. Embed the question
    embedder = Embedder()
    query_embedding = embedder.embed(query)

    # 2. Retrieve relevant chunks
    results = search_similar(
        query_embedding=query_embedding,
        top_k=3,
    )

    # 3. Build context
    context = build_context(results)

    # 4. Build user prompt
    user_prompt = build_user_prompt(
        query=query,
        context=context,
    )

    print("=" * 70)
    print("SYSTEM PROMPT")
    print("=" * 70)
    print(SYSTEM_PROMPT)

    print("\n" + "=" * 70)
    print("USER PROMPT")
    print("=" * 70)
    print(user_prompt)


if __name__ == "__main__":
    main()