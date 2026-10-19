"""
Stores embeddings and runs similarity search with pgvector.
"""
import psycopg
from app.core.config import settings

def get_db_config() -> dict:
    """
    Return PostgreSQL connection settings.
    """
    return {
        "host": settings.db_host,
        "port": settings.db_port,
        "dbname": settings.db_name,
        "user": settings.db_user,
        "password": settings.db_password,
        "connect_timeout": 5,
    }


def insert_chunk(
    document_id: str,
    document_name: str,
    page_number: int,
    section: str,
    chunk_text: str,
    embedding: list[float],
    embedding_model: str,
) -> None:
    """
    Insert a document chunk and its embedding into PostgreSQL.
    """

    with psycopg.connect(**get_db_config()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO document_chunks (
                    document_id,
                    document_name,
                    page_number,
                    section,
                    chunk_text,
                    embedding,
                    embedding_model
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    document_id,
                    document_name,
                    page_number,
                    section,
                    chunk_text,
                    embedding,
                    embedding_model,
                ),
            )


def search_similar(query_embedding: list[float],top_k: int = 3) -> list[dict]:
    """
    Retrieve the top-K chunks by cosine distance.
    """
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    with psycopg.connect(**get_db_config()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    document_name,
                    page_number,
                    section,
                    chunk_text,
                    embedding_model,
                    embedding <=> %s::vector AS distance
                FROM document_chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
                """,
                (query_embedding, query_embedding, top_k),
            )
            rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "document_name": row[1],
            "page_number": row[2],
            "section": row[3],
            "chunk_text": row[4],
            "embedding_model": row[5],
            "distance": row[6],
        }
        for row in rows
    ]
