from langchain_community.document_loaders import PyPDFLoader

# Load first PDF
loader1 = PyPDFLoader("data/godrej.pdf")
godrej_documents = loader1.load()

# Load second PDF
loader2 = PyPDFLoader("data/jsw.pdf")
jsw_documents = loader2.load()

# Combine both documents
documents = godrej_documents + jsw_documents

print(f"Total pages/documents loaded: {len(documents)}")

for doc in documents:
    print("\nSOURCE:", doc.metadata["source"])
    print("CONTENT:", doc.page_content[:300])