from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from langchain_qdrant import QdrantVectorStore

from text_splitter import chunks
from embeddings import embeddings


# ==========================================
# CREATE LOCAL QDRANT DATABASE
# ==========================================

client = QdrantClient(
    path="./qdrant_data"
)


# ==========================================
# COLLECTION NAME
# ==========================================

collection_name = "company_reports"


# ==========================================
# DELETE OLD COLLECTION
# ==========================================

try:
    client.delete_collection(collection_name)
    print("Old collection deleted.")

except Exception:
    print("Creating new collection.")


# ==========================================
# CREATE COLLECTION
# ==========================================

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)


# ==========================================
# CONNECT LANGCHAIN + QDRANT
# ==========================================

vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings
)


# ==========================================
# STORE DOCUMENTS
# ==========================================

vector_store.add_documents(
    documents=chunks
)


print("Successfully stored documents in Qdrant!")
print("Total chunks stored:", len(chunks))