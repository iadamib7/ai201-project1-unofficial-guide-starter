from src.retrieve import retrieve
from src.generate import generate_answer


def ask(question: str):
    retrieved_chunks = retrieve(question, k=5)
    result = generate_answer(question, retrieved_chunks)
    return result


if __name__ == "__main__":
    question = input("Ask a question: ")
    result = ask(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source}")
        