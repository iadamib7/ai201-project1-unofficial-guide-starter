import chromadb
from sentence_transformers import SentenceTransformer

from src.chunk import build_chunks


DB_DIR = "chroma_db"
COLLECTION_NAME = "unofficial_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def build_vector_store():
    chunks = build_chunks()

    if not chunks:
        raise ValueError("No chunks found. Add .txt files to the documents folder first.")

    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts).tolist()

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
    