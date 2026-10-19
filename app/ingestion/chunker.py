import re

SECTION_PATTERN = re.compile(r"^\d+\.\s+.+$")

def chunk_pages(pages: list[dict]) -> list[dict]:
    """
    Convert extracted PDF pages into section-aware chunks.

    Each chunk contains:
        page_number
        section
        text
    """

    chunks = []

    current_section = None
    current_page = None
    current_lines = []

    def save_current_chunk():
        if current_lines and current_section:
            chunks.append(
                {
                    "page_number": current_page,
                    "section": current_section,
                    "text": "\n".join(current_lines).strip(),
                }
            )

    for page in pages:
        page_number = page["page_number"]

        for line in page["text"].splitlines():
            line = line.strip()

            if not line:
                continue

            if SECTION_PATTERN.match(line):
                save_current_chunk()

                current_section = line
                current_page = page_number
                current_lines = []
            else:
                current_lines.append(line)

    save_current_chunk()

    return chunks