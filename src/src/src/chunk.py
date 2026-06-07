from src.ingest import load_documents


CHUNK_SIZE = 800
OVERLAP = 120


def split_into_paragraphs(text: str):
    """
    Split text into paragraphs. If the text has no paragraph breaks,
    fall back to sentence-like splitting.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    if len(paragraphs) <= 1:
        paragraphs = [p.strip() for p in text.split(". ") if p.strip()]

    return paragraphs


def chunk_text(text: str, source: str):
    """
    Combine paragraphs into chunks around CHUNK_SIZE characters,
    with a small overlap to preserve context.
    """
    paragraphs = split_into_paragraphs(text)

    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 1 <= CHUNK_SIZE:
            current = f"{current} {paragraph}".strip()
        else:
            if current:
                chunks.append(current)

            overlap_text = current[-OVERLAP:] if current else ""
            current = f"{overlap_text} {paragraph}".strip()

    if current:
        chunks.append(current)

    chunk_records = []

    for index, chunk in enumerate(chunks):
        if chunk.strip():
            chunk_records.append(
                {
                    "source": source,
                    "chunk_id": index,
                    "text": chunk.strip(),
                }
            )

    return chunk_records


def build_chunks():
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"], doc["source"])
        all_chunks.extend(chunks)

    return all_chunks


if __name__ == "__main__":
    chunks = build_chunks()
    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks[:5]:
        print("-" * 80)
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["text"])
        