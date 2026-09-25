# Module 3 — Support Assistant

A RAG-based Zepto customer support assistant built using LangGraph, ChromaDB, Sentence Transformers, FastAPI, and Pydantic.

## Technologies

- Python
- LangGraph
- ChromaDB
- Sentence Transformers
- FastAPI
- Pydantic
- Docker

## Project Structure

```text
support_assistant/
├── data/
│   └── chroma_db/
├── docs/
│   ├── doc1.txt
│   ├── doc2.txt
│   ├── doc3.txt
│   ├── doc4.txt
│   ├── doc5.txt
│   ├── doc6.txt
│   ├── doc7.txt
│   └── doc8.txt
├── ingest.py
├── retrieve.py
├── models.py
├── prompts.py
├── graph.py
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
├── test_graph.py
├── test_models.py
└── test_prompt.py


{
  "query": "What is the capital of India?"
}


{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}



{
  "query": "What is the delivery fee?"
}


{
  "answer": "Standard delivery is free on orders over INR 149; orders below this threshold incur a flat INR 25 delivery fee.",
  "sources": [
    "doc1",
    "doc5",
    "doc2"
  ],
  "confidence": 1.0
}

