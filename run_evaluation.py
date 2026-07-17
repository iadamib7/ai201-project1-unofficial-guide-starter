from src.query import ask

questions = [
    "What do students say is the most useful thing about the course or resource?",
    "What problems or complaints do students mention most often?",
    "What advice do students give to someone taking the course or using the resource?",
    "What positive feedback do students give?",
    "Which professor should I take next semester?",
]

for number, question in enumerate(questions, start=1):
    print("=" * 90)
    print(f"QUESTION {number}: {question}")
    result = ask(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")
    if result["sources"]:
        for source in result["sources"]:
            print(f"- {source}")
    else:
        print("No relevant sources found.")

    print("\nRETRIEVED CHUNKS:")
    if result["retrieved_chunks"]:
        for chunk in result["retrieved_chunks"]:
            print(
                f"- {chunk['source']} | chunk {chunk['chunk_id']} "
                f"| distance {chunk['distance']:.4f}"
            )
            print(chunk["text"])
            print()
    else:
        print("No relevant chunks found.")
