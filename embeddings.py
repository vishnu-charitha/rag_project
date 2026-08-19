from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

if __name__ == "__main__":
    text = "What are the sustainability initiatives of JSW Steel?"

    vector = embeddings.embed_query(text)

    print("First 10 values:")
    print(vector[:10])

    print("\nVector length:")
    print(len(vector))