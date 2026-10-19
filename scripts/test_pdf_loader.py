from app.ingestion.pdf_loader import extract_pages

PDF_PATH = "data/acme-simple_employee_leave_policy.pdf"

pages = extract_pages(PDF_PATH)

print(f"Pages extracted: {len(pages)}")

for page in pages:
    print("=" * 80)
    print(f"PAGE {page['page_number']}")
    print("=" * 80)

    print(page["text"][:1500])
    print()