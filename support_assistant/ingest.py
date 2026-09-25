from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# 1. Load documents
# --------------------------------------------------

DOCS_DIR = Path("docs")

documents = []

for file_path in sorted(DOCS_DIR.glob("*.txt")):
    text = file_path.read_text(encoding="utf-8")

    documents.append({
        "id": file_path.stem,
        "text": text
    })

print("Documents loaded:", len(documents))


# --------------------------------------------------
# 2. Load embedding model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# --------------------------------------------------
# 3. Generate embeddings
# --------------------------------------------------

texts = [document["text"] for document in documents]
ids = [document["id"] for document in documents]

embeddings = model.encode(texts)

print("Embeddings created:", len(embeddings))
print("Embedding size:", len(embeddings[0]))


# --------------------------------------------------
# 4. Create ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="data/chroma_db"
)


# --------------------------------------------------
# 5. Create collection
# --------------------------------------------------

collection = client.get_or_create_collection(
    name="zepto_policies",
    metadata={
        "hnsw:space": "cosine"
    }
)


# --------------------------------------------------
# 6. Store documents + embeddings
# --------------------------------------------------

collection.upsert(
    ids=ids,
    documents=texts,
    embeddings=embeddings.tolist()
)


print("Documents stored in ChromaDB:", collection.count())