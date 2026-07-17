from src.ingest import load_documents

CHUNK_SIZE = 800
OVERLAP = 150

def split_into_paragraphs(text: str):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    if len(paragraphs) <= 1:
        paragraphs = [p.strip() for p in text.split(". ") if p.strip()]

    return paragraphs

def chunk_text(text: str, source: str):
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

    return [
        {
            "source": source,
            "chunk_id": index,
            "text": chunk.strip(),
        }
        for index, chunk in enumerate(chunks)
        if chunk.strip()
    ]

def build_chunks():
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        all_chunks.extend(chunk_text(doc["text"], doc["source"]))

    return all_chunks

if __name__ == "__main__":
    chunks = build_chunks()
    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks[:5]:
        print("-" * 80)
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["text"])
