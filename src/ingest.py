"""
src/ingest.py — The Unofficial Guide

Loads and cleans text documents from the documents folder.
"""

from pathlib import Path
import re


DOCUMENTS_DIR = Path("documents")


def clean_text(text: str) -> str:
    """
    Clean document text before chunking.

    Removes UTF-8 BOM characters, normalizes line endings, removes
    repeated whitespace, and drops empty lines.
    """
    text = text.replace("\ufeff", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    cleaned_lines = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            cleaned_lines.append("")
            continue

        line = re.sub(r"\s+", " ", line)
        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)

    # Keep paragraph breaks, but collapse excessive blank lines.
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

    return cleaned_text.strip()


def load_documents() -> list[dict]:
    """
    Load all .txt documents from the documents directory.

    Returns:
        A list of dictionaries containing:
        - source: original filename
        - text: cleaned document text

    Raises:
        FileNotFoundError: If the documents directory does not exist.
        ValueError: If no usable text documents are found.
    """
    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"Documents directory not found: {DOCUMENTS_DIR.resolve()}"
        )

    documents = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        # utf-8-sig automatically removes a UTF-8 BOM when present.
        raw_text = file_path.read_text(
            encoding="utf-8-sig",
            errors="replace",
        )

        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            continue

        documents.append(
            {
                "source": file_path.name,
                "text": cleaned_text,
            }
        )

    if not documents:
        raise ValueError(
            "No usable .txt documents were found in the documents folder."
        )

    return documents


if __name__ == "__main__":
    loaded_documents = load_documents()

    print(f"Loaded {len(loaded_documents)} documents.")

    for document in loaded_documents:
        print("-" * 80)
        print(f"Source: {document['source']}")
        print(document["text"][:500])
