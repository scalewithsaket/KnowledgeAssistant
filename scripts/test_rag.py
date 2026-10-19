import sys

sys.stdout.reconfigure(encoding="utf-8")

from app.ingestion.embedder import Embedder
from app.storage.vector_store import search_similar
from app.rag.context_builder import build_context
from app.rag.prompt_builder import (
    SYSTEM_PROMPT,
    build_user_prompt,
)
from app.llm.groq_client import GroqClient


def main():
    query = "How many casual leaves can an employee take?"

    # 1. Convert question into embedding
    embedder = Embedder()
    query_embedding = embedder.embed(query)

    # 2. Retrieve relevant chunks
    results = search_similar(
        query_embedding=query_embedding,
        top_k=3,
    )

    # 3. Build context from retrieved chunks
    context = build_context(results)

    # 4. Build LLM prompt
    user_prompt = build_user_prompt(query=query, context=context)

    # 5. Generate answer
    groq = GroqClient()

    print("\n" + "=" * 70)
    print("CONTEXT SENT TO GROQ")
    print("=" * 70)
    print(context)

    answer = groq.generate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)

    print("\n" + "=" * 70)
    print("ANSWER REPR")
    print("=" * 70)
    print(repr(answer))

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(answer)

    for result in results:
        print(
            f"Distance: {result['distance']:.4f} | "
            f"{result['section']}"
        )

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(answer)

if __name__ == "__main__":
    main()
