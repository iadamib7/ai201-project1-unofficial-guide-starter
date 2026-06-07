import gradio as gr

from src.query import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", "", ""

    result = ask(question)

    answer = result["answer"]
    sources = "\n".join(f"- {source}" for source in result["sources"])

    retrieved_chunks = "\n\n".join(
        f"""
Source: {chunk["source"]}
Chunk ID: {chunk["chunk_id"]}
Distance: {chunk["distance"]:.4f}

{chunk["text"]}
""".strip()
        for chunk in result["retrieved_chunks"]
    )

    return answer, sources, retrieved_chunks

with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide")
    gr.Markdown("Ask a question about the student-generated documents in the `documents` folder.")

    question = gr.Textbox(
        label="Your question",
        placeholder="What do students say about workload?"
    )

    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=5)
    retrieved = gr.Textbox(label="Retrieved Chunks", lines=12)

    ask_button.click(
        handle_query,
        inputs=question,
        outputs=[answer, sources, retrieved],
    )

    question.submit(
        handle_query,
        inputs=question,
        outputs=[answer, sources, retrieved],
    )

if __name__ == "__main__":
    demo.launch()
