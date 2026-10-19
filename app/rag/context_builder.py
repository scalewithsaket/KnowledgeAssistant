def build_context(results: list[dict]) -> str:
    context_parts = []

    for index, result in enumerate(results, start=1):

        source = (
            f"[Source {index}]\n"
            f"Document: {result['document_name']}\n"
            f"Page: {result['page_number']}\n"
            f"Section: {result['section']}\n"
        )

        content = (
            f"Content:\n"
            f"{result['chunk_text']}"
        )

        context_parts.append(
            f"{source}{content}"
        )

    return "\n\n".join(context_parts)