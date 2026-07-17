# The Unofficial Guide

A Retrieval-Augmented Generation (RAG) system that helps students search and explore student-generated course information, academic resources, workload advice, and course feedback.

---

## Project Overview

Students often rely on scattered course reviews, discussion posts, and informal advice when choosing classes or finding academic resources.

This project builds a Retrieval-Augmented Generation (RAG) pipeline that:

1. Stores student-related documents in a vector database.
2. Retrieves the most relevant document chunks for a question.
3. Uses a language model to generate a grounded answer from retrieved evidence.
4. Refuses to answer when the information is not present in the document collection.

---

## Architecture

User Question
↓
Semantic Embedding (all-MiniLM-L6-v2)
↓
ChromaDB Similarity Search
↓
Top Relevant Chunks
↓
Groq LLM Generation
↓
Grounded Answer + Sources

---

## Document Processing

Documents are stored in the `documents/` directory.

The ingestion pipeline:

- Loads `.txt` files
- Removes UTF-8 BOM characters
- Normalizes whitespace
- Preserves paragraph structure

Chunking settings:

- Chunk Size: 800 characters
- Overlap: 150 characters

---

## Embedding Model

Model:

```
sentence-transformers/all-MiniLM-L6-v2
```

This model produces 384-dimensional semantic embeddings.

### Revision Note

During project revision, I discovered that an earlier implementation used a custom hash-based embedding function rather than semantic embeddings.

I replaced that implementation with the documented `all-MiniLM-L6-v2` model and rebuilt the vector database to improve retrieval quality.

---

## Vector Database

Database:

```
ChromaDB
```

Stored:

- Chunk text
- Source filename
- Chunk ID
- Semantic embedding vector

---

## Retrieval Strategy

For each query:

1. Generate semantic embedding.
2. Search ChromaDB for the nearest chunks.
3. Filter weak matches using a distance threshold.
4. Return only sufficiently relevant chunks.

This reduces unrelated retrieval results and improves answer quality.

---

## Out-of-Scope Handling

If retrieval finds no sufficiently relevant chunks:

- No sources are displayed.
- No chunks are displayed.
- The system returns:

> I don't have enough information in the provided documents to answer that.

This prevents hallucinated answers.

---

## Evaluation

### Question 1

**Why are student course reviews useful?**

Retrieved information showed that course reviews:

- Supplement official course descriptions.
- Provide real student experiences.
- Help students make informed course choices.

---

### Question 2

**What resources help students with writing assignments?**

Retrieved information identified:

- Writing centers
- One-on-one tutoring
- Workshops
- Drop-in support

---

### Question 3

**Why do students care about workload before choosing a class?**

Retrieved information showed that:

- Workload influences course planning.
- Students want realistic expectations.
- Time commitment affects course selection.

---

### Unsupported Question

**What is photosynthesis?**

Result:

> I don't have enough information in the provided documents to answer that.

This demonstrates correct refusal behavior when the information is absent from the document collection.

---

## Technologies Used

- Python
- ChromaDB
- Sentence Transformers
- Groq API
- Gradio
- python-dotenv

---

## Limitations

Current limitations:

1. Small document collection (18 chunks).
2. Documents are mostly summaries rather than raw student reviews.
3. Retrieval quality depends heavily on document coverage.
4. No reranking stage is used.

Future improvements:

- Larger student review dataset.
- Hybrid retrieval (keyword + vector search).
- Retrieval reranking.
- Citation highlighting.

---

## AI Usage

I used AI tools for:

- Debugging Python code
- Understanding retrieval errors
- Refactoring project structure
- Improving documentation

All code was reviewed, modified, tested, and integrated by me.