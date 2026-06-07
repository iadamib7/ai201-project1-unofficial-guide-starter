import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

MODEL_NAME = "llama-3.3-70b-versatile"


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

    return Groq(api_key=api_key)


def format_context(retrieved_chunks):
    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"""
[Source {index}]
Document: {chunk["source"]}
Chunk ID: {chunk["chunk_id"]}

{chunk["text"]}
""".strip()
        )

    return "\n\n".join(context_parts)


def generate_answer(question: str, retrieved_chunks):
    client = get_groq_client()
    context = format_context(retrieved_chunks)

    system_prompt = """
You are a grounded question-answering assistant.

Answer the user's question using only the provided context.
Do not use outside knowledge.
If the context does not contain enough information to answer, say:
"I don't have enough information in the provided documents to answer that."

Always mention the source document names used in your answer.
""".strip()

    user_prompt = f"""
Question:
{question}

Context:
{context}
""".strip()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    sources = sorted(
        {
            f"{chunk['source']} | chunk {chunk['chunk_id']}"
            for chunk in retrieved_chunks
        }
    )

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }
