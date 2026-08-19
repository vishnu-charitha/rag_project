from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from langchain_qdrant import QdrantVectorStore
from embeddings import embeddings


client = QdrantClient(path="./qdrant_data")


vector_store = QdrantVectorStore(
    client=client,
    collection_name="company_reports",
    embedding=embeddings
)


def retrieve_documents(query, k=3):

    search_filter = Filter(
        must=[
            FieldCondition(
                key="metadata.source",
                match=MatchValue(value="data/jsw.pdf")
            )
        ]
    )

    return vector_store.similarity_search(
        query=query,
        k=k,
        filter=search_filter
    )


def close_qdrant():
    client.close()


if __name__ == "__main__":

    question = "What are the greenhouse gas reduction initiatives of JSW?"

    results = retrieve_documents(question, k=1)

    for i, doc in enumerate(results):
        print(f"\n--- RESULT {i+1} ---")
        print("Source:", doc.metadata.get("source"))
        print("Page:", doc.metadata.get("page"))
        print("\nContent:")
        print(doc.page_content)

    close_qdrant()