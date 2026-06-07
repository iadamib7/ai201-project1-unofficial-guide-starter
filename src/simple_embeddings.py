import hashlib
import math
import re


EMBEDDING_DIM = 384


def tokenize(text: str):
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def embed_text(text: str):
    """
    Simple local hash-based embedding.

    This avoids sentence-transformers because some Windows systems block
    scikit-learn DLL files used by that package.
    """
    vector = [0.0] * EMBEDDING_DIM
    tokens = tokenize(text)

    for token in tokens:
        digest = hashlib.md5(token.encode("utf-8")).hexdigest()
        index = int(digest, 16) % EMBEDDING_DIM
        vector[index] += 1.0

    norm = math.sqrt(sum(value * value for value in vector))

    if norm == 0:
        return vector

    return [value / norm for value in vector]
