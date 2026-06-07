from pathlib import Path
import re


DOCUMENTS_DIR = Path("documents")


def clean_text(text: str) -> str:
    """
    Clean raw document text by removing extra whitespace and simple artifacts.
    """
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def load_documents():
    """
    Load all .txt files from the documents folder.
    Returns a list of dictionaries with source filename and cleaned text.
    """
    documents = []

    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError("The documents folder does not exist.")

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned = clean_text(raw_text)

        if cleaned:
            documents.append(
                {
                    "source": file_path.name,
                    "text": cleaned,
                }
            )

    return documents


if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.")

    for doc in docs:
        print("-" * 80)
        print(f"Source: {doc['source']}")
        print(doc["text"][:500])

        