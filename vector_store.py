from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_qdrant import QdrantVectorStore

from text_splitter import chunks
from embeddings import embeddings


# Create local Qdrant database
client = QdrantClient(path="./qdrant_data")


# Collection name
collection_name = "company_reports"


# Delete old collection if it already exists
try:
    client.delete_collection(collection_name)
except Exception:
    pass


# Create a new collection
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)


# Connect LangChain with Qdrant
vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings
)


# Store all chunks
vector_store.add_documents(chunks)


print("Successfully stored documents in Qdrant!")
print("Total chunks stored:", len(chunks))