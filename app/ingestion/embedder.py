"""
Creates normalized embeddings using Sentence Transformers.
With embeddings, we can retrieve based on intent, paraphrase, and conceptual similarity.
"""
from sentence_transformers import SentenceTransformer
from app.core.config import settings


class Embedder:
    """
    Generate normalized text embeddings.
    """
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)

    def embed(self, text: str) -> list[float]:
        """Encode text as a normalized embedding vector."""
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()