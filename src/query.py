from src.generate import generate_answer
from src.retrieve import retrieve


REFUSAL_MESSAGE = (
    "I don't have enough information in the provided documents to answer that."
)


def ask(question: str) -> dict:
    """
    Run the complete retrieval and generation pipeline.

    If retrieval finds no sufficiently relevant chunks, return a refusal
    without calling the language model or displaying unrelated sources.
    """
    if not question or not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "retrieved_chunks": [],
        }

    retrieved_chunks = retrieve(question, k=5)

    if not retrieved_chunks:
        return {
            "answer": REFUSAL_MESSAGE,
            "sources": [],
            "retrieved_chunks": [],
        }

    return generate_answer(question, retrieved_chunks)


if __name__ == "__main__":
    question = input("Ask a question: ")
    result = ask(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    if result["sources"]:
        for source in result["sources"]:
            print(f"- {source}")
    else:
        print("No relevant sources found.")