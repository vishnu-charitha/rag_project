from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from langchain_qdrant import QdrantVectorStore
from embeddings import embeddings


# ==========================================
# CONNECT TO QDRANT
# ==========================================

client = QdrantClient(
    path="./qdrant_data"
)

collection_name = "company_reports"


# ==========================================
# CREATE VECTOR STORE
# ==========================================

vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings
)


# ==========================================
# RETRIEVE DOCUMENTS
# ==========================================

def retrieve_documents(query, k=3):

    query_lower = query.lower()

    search_filter = None

    # --------------------------------------
    # GODREJ FILTER
    # --------------------------------------

    if "godrej" in query_lower:

        print("Company detected: Godrej")

        search_filter = Filter(
            must=[
                FieldCondition(
                    key="metadata.company",
                    match=MatchValue(
                        value="godrej"
                    )
                )
            ]
        )

    # --------------------------------------
    # JSW FILTER
    # --------------------------------------

    elif "jsw" in query_lower:

        print("Company detected: JSW")

        search_filter = Filter(
            must=[
                FieldCondition(
                    key="metadata.company",
                    match=MatchValue(
                        value="jsw"
                    )
                )
            ]
        )

    # --------------------------------------
    # NO COMPANY FILTER
    # --------------------------------------

    else:

        print("No company filter applied.")

    # --------------------------------------
    # SEARCH QDRANT
    # --------------------------------------

    return vector_store.similarity_search(
        query=query,
        k=k,
        filter=search_filter
    )


# ==========================================
# CLOSE QDRANT
# ==========================================

def close_qdrant():

    client.close()


# ==========================================
# TEST RETRIEVER
# ==========================================

if __name__ == "__main__":

    question = (
        "What are the greenhouse gas "
        "reduction initiatives of JSW?"
    )

    results = retrieve_documents(
        question,
        k=3
    )

    for i, doc in enumerate(results):

        print(f"\n--- RESULT {i + 1} ---")

        print(
            "Company:",
            doc.metadata.get("company")
        )

        print(
            "Source:",
            doc.metadata.get("source")
        )

        print(
            "Page:",
            doc.metadata.get("page")
        )

        print("\nContent:")
        print(doc.page_content)

    close_qdrant()