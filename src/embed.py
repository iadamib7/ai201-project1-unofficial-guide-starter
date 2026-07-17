import chromadb

from src.chunk import build_chunks
from src.simple_embeddings import embed_texts


DB_DIR = "chroma_db"
COLLECTION_NAME = "unofficial_guide"


def build_vector_store():
    chunks = build_chunks()

    if not chunks:
        raise ValueError("No chunks found. Add .txt files to the documents folder first.")

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts)

    client = chromadb.PersistentClient(path=DB_DIR)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    ids = [f"{chunk['source']}-{chunk['chunk_id']}" for chunk in chunks]

    metadatas = [
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")


if __name__ == "__main__":
    build_vector_store()
