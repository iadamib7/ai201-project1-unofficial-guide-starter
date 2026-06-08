# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

My domain is student experiences and advice about college courses, professors, and academic resources.

This knowledge is valuable because official school pages usually describe courses in a formal way, but they do not always explain what students actually experience. Students often want to know things like how hard a class feels, what problems other students mention, what resources are useful, and what advice previous students would give.

This information can be hard to find because it is spread across student reviews, posts, comments, and informal documents instead of being organized in one official place. My system will make this unofficial student knowledge searchable through a question-answering interface.

---

## Documents

I collected documents from the following sources:

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|

| 1 | Test reviews | Student review text used for retrieval testing | documents/test_reviews.txt |
| 2 | Rate My Professors overview | Background on student professor ratings and class choice | documents/course_review_2.txt |
| 3 | Critical Review at Brown University | Example of student-written course reviews | documents/course_review_3.txt |
| 4 | Student Q&A forum research | Student behavior and discomfort in course forums | documents/course_review_4.txt |
| 5 | Course review sentiment analysis | Research on organizing open-ended student course feedback | documents/course_review_5.txt |
| 6 | Carnegie rule workload background | Background on course workload and study-time expectations | documents/student_advice_6.txt |
| 7 | Writing center overview | Notes on academic support for writing assignments | documents/student_advice_7.txt |
| 8 | Student SPILL peer support | Example of anonymous peer support for students | documents/resource_feedback_8.txt |
| 9 | Ask Foy information service | Example of a student-facing campus information service | documents/resource_feedback_9.txt |
| 10 | MOOC discussion forum research | Notes on student discussion posts and course content | documents/course_feedback_10.txt |

These sources cover different student perspectives, including course difficulty, workload, useful resources, common complaints, and advice for future students.
---

## Chunking Strategy

**Chunk size:** 800 characters

**Overlap:** 150 characters

**Reasoning:**

I chose 800-character chunks because my documents are mostly short or medium-length student-written text. A chunk this size is large enough to keep a complete idea together, but not so large that unrelated topics are mixed into the same chunk.

The 150-character overlap helps protect information that might appear near the boundary between two chunks. If a student comment or important detail is split between chunks, the overlap increases the chance that retrieval still returns enough context.

If chunks are too small, the system may retrieve fragments that do not make sense by themselves. If chunks are too large, the system may retrieve text that contains too many unrelated ideas, making the generated answer less focused.

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` using `sentence-transformers`

**Top-k:** 5

**Production tradeoff reflection:**

I am using `all-MiniLM-L6-v2` because it runs locally, is free, and works well for semantic search on small projects. It does not require paid API credits, which makes it a good fit for this assignment.

For each user query, I will retrieve the top 5 most relevant chunks from the vector store. This should provide enough context for the LLM without giving it too much unrelated information.

If I were deploying this for real users and cost was not a constraint, I would compare embedding models based on accuracy, context length, speed, multilingual support, and cost. I would also consider whether the model handles student language, slang, and informal reviews well. For a larger production system, I might use a stronger embedding model or hybrid search to combine semantic search with keyword matching.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say is the most useful thing about the course or resource? | The system should summarize the main useful resource or benefit mentioned in the collected documents and cite the source document. |
| 2 | What problems or complaints do students mention most often? | The system should identify common complaints from the documents, such as workload, unclear instructions, difficulty, or lack of information, depending on the source text. |
| 3 | What advice do students give to someone taking the course or using the resource? | The system should return advice that appears in the documents, such as starting early, using available resources, asking for help, or reading instructions carefully. |
| 4 | What positive feedback do students give? | The system should summarize positive comments from the documents and cite where the information came from. |
| 5 | Which professor should I take next semester? | The system should either give a limited answer based only on the available documents or say it does not have enough information if the documents do not directly support a recommendation. |

Each question is designed to test whether the system retrieves relevant chunks and generates an answer grounded in the documents. Question 5 is also useful as a failure or limitation case because it asks for a recommendation that may require information outside the collected sources.

---

## Anticipated Challenges

1. Some documents may contain noisy or inconsistent text. Student-written sources can include repeated headers, copied navigation text, unrelated comments, formatting problems, or incomplete sentences. This could make the chunks less useful if the cleaning step does not remove the noise.

2. Retrieval may return partially relevant chunks instead of the best evidence. If chunks are too short, they may not contain enough context. If chunks are too long, they may include multiple unrelated topics. I will inspect sample chunks and test retrieval before relying on generation.

3. Source attribution could be incomplete if metadata is not saved correctly. Each chunk needs to keep track of its source document so the final answer can show where the information came from.

---

## Architecture

```mermaid
flowchart TD
    A[Document Ingestion<br>Load text files from data folder] --> B[Cleaning<br>Remove empty text, extra spaces, and irrelevant formatting]
    B --> C[Chunking<br>800-character chunks with 150-character overlap]
    C --> D[Embeddings<br>sentence-transformers all-MiniLM-L6-v2]
    D --> E[Vector Store<br>ChromaDB with source metadata]
    E --> F[Retrieval<br>Return top 5 relevant chunks]
    F --> G[Generation<br>LLM answers using retrieved context only]
    G --> H[Query Interface<br>Display answer and sources]