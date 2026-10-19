from app.ingestion.pdf_loader import extract_pages
from app.ingestion.chunker import chunk_pages
from app.ingestion.embedder import Embedder

PDF_PATH = "data/acme-simple_employee_leave_policy.pdf"

def main():
    # 1. Extract PDF pages
    pages = extract_pages(PDF_PATH)

    # 2. Create logical chunks
    chunks = chunk_pages(pages)

    # 3. Load embedding model
    embedder = Embedder()

    # 4. Take one chunk
    chunk = chunks[1]

    print("Section:")
    print(chunk["section"])

    print("\nChunk text:")
    print(chunk["text"])

    # 5. Generate embedding
    embedding = embedder.embed(chunk["text"])

    print("\nEmbedding information:")
    print("Type:", type(embedding))
    print("Dimensions:", len(embedding))
    print("First 10 values:", embedding[:10])


if __name__ == "__main__":
    main()