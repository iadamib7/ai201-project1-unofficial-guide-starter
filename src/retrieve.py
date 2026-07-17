import chromadb

from src.simple_embeddings import embed_text


DB_DIR = "chroma_db"
COLLECTION_NAME = "unofficial_guide"
MAX_DISTANCE = 1.20


client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_collection(name=COLLECTION_NAME)


def retrieve(query: str, k: int = 5) -> list[dict]:
    """
    Retrieve the most relevant chunks for a query.

    Results with weak similarity scores are filtered out so unrelated
    documents are not passed to the generation step.

    Args:
        query: The user's question.
        k: Maximum number of candidate chunks to retrieve.

    Returns:
        A list of relevant chunk dictionaries.
    """
    if not query or not query.strip():
        return []

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved_chunks = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        if distance is None or distance > MAX_DISTANCE:
            continue

        retrieved_chunks.append(
            {
                "text": document,
                "source": metadata["source"],
                "chunk_id": metadata["chunk_id"],
                "distance": float(distance),
            }
        )

    return retrieved_chunks


if __name__ == "__main__":
    question = input("Ask a question: ")
    results = retrieve(question)

    if not results:
        print("No sufficiently relevant chunks were found.")
    else:
        for result in results:
            print("-" * 80)
            print(f"Source: {result['source']}")
            print(f"Chunk ID: {result['chunk_id']}")
            print(f"Distance: {result['distance']:.4f}")
            print(result["text"])