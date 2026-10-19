from app.ingestion.pdf_loader import extract_pages
from app.ingestion.chunker import chunk_pages

PDF_PATH = "data/acme-simple_employee_leave_policy.pdf"

pages = extract_pages(PDF_PATH)

chunks = chunk_pages(pages)

print(f"Total chunks: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print("=" * 80)
    print(f"CHUNK {index}")
    print(f"Page: {chunk['page_number']}")
    print(f"Section: {chunk['section']}")
    print("=" * 80)
    print(chunk["text"])
    print()