"""
The RAG Service orchestration layer.
"""
from app.ingestion.embedder import Embedder
from app.storage.vector_store import search_similar
from app.rag.context_builder import build_context
from app.rag.prompt_builder import SYSTEM_PROMPT, build_user_prompt
from app.llm.groq_client import GroqClient
from app.core.config import settings

class RAGService:
    """
    Orchestrate retrieval-augmented question answering.
    """
    def __init__(self):
        self.embedder = Embedder()
        self.groq_client = GroqClient()

    def query(self, question: str, top_k: int = 3) -> dict:
        """
        Answer a question using retrieved document context.
        """

        # 1. Embed the question
        query_embedding = self.embedder.embed(question)

        # 2. Retrieve relevant document chunks
        results = search_similar(query_embedding=query_embedding, top_k=top_k)

        if not results or results[0]["distance"] > settings.retrieval_distance_threshold:
            return {
                "question": question,
                "answer": (
                    "I don't have sufficient information to answer "
                    "this question from the available documents."
                ),
                "context": "",
                "sources": [],
            }

        # 3. Build context from retrieved chunks
        context = build_context(results)

        # 4. Build the LLM prompt
        user_prompt = build_user_prompt(query=question, context=context)

        # 5. Generate the answer
        answer = self.groq_client.generate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)

        # 6. Return the result
        return {
            "question": question,
            "answer": answer,
            "context": context,
            "sources": results,
        }
