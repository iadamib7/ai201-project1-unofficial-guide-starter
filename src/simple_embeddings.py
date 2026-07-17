from functools import lru_cache

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load and cache the semantic embedding model."""
    return SentenceTransformer(MODEL_NAME)


def embed_text(text: str) -> list[float]:
    """
    Convert text into a semantic embedding using all-MiniLM-L6-v2.

    Args:
        text: The text to embed.

    Returns:
        A normalized 384-dimensional embedding vector.
    """
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text")

    model = get_embedding_model()
    embedding = model.encode(
        text,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    return embedding.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert multiple texts into semantic embeddings efficiently.
    """
    if not texts:
        return []

    if any(not text or not text.strip() for text in texts):
        raise ValueError("Cannot embed empty text")

    model = get_embedding_model()
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True,
    )
    return embeddings.tolist()