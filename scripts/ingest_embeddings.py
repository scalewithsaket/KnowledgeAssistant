from app.ingestion.pdf_loader import extract_pages
from app.ingestion.chunker import chunk_pages
from app.ingestion.embedder import Embedder
from app.storage.vector_store import insert_chunk

PDF_PATH = "data/acme-simple_employee_leave_policy.pdf"
DOCUMENT_ID = "HR-LEAVE-001"
DOCUMENT_NAME = "acme-simple_employee_leave_policy.pdf"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def main():
    # Extract PDF
    pages = extract_pages(PDF_PATH)

    # Create logical chunks
    chunks = chunk_pages(pages)

    # Section 7 contains evaluation data.
    knowledge_chunks = chunks[:6]

    # Load embedding model once
    embedder = Embedder()

    for chunk in knowledge_chunks:

        embedding = embedder.embed(chunk["text"])

        insert_chunk(
            document_id=DOCUMENT_ID,
            document_name=DOCUMENT_NAME,
            page_number=chunk["page_number"],
            section=chunk["section"],
            chunk_text=chunk["text"],
            embedding=embedding,
            embedding_model=MODEL_NAME,
        )

        print(
            f"Inserted: {chunk['section']} "
            f"({len(embedding)} dimensions)"
        )

if __name__ == "__main__":
    main()