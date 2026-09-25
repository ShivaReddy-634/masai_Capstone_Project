import chromadb
from sentence_transformers import SentenceTransformer


# ---------------------------------------
# 1. Load embedding model
# ---------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------------------
# 2. Connect to ChromaDB
# ---------------------------------------

client = chromadb.PersistentClient(
    path="data/chroma_db"
)


# ---------------------------------------
# 3. Get our collection
# ---------------------------------------

collection = client.get_collection(
    name="zepto_policies"
)


# ---------------------------------------
# 4. User query
# ---------------------------------------

query = "What is the delivery fee?"


# ---------------------------------------
# 5. Convert query into embedding
# ---------------------------------------

query_embedding = model.encode(
    [query]
).tolist()


# ---------------------------------------
# 6. Retrieve top 3 documents
# ---------------------------------------

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)


# ---------------------------------------
# 7. Display results
# ---------------------------------------

print("\nQuery:")
print(query)

print("\nRetrieved documents:")

for i, document in enumerate(results["documents"][0]):
    print("\n----------------------------")
    print("Rank:", i + 1)
    print("Document:", results["ids"][0][i])
    print("Content:")
    print(document)