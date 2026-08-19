from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import documents

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Total chunks:", len(chunks))

# Count chunks from each PDF
godrej_count = 0
jsw_count = 0

for chunk in chunks:
    source = chunk.metadata["source"]

    if "godrej.pdf" in source:
        godrej_count += 1
    elif "jsw.pdf" in source:
        jsw_count += 1

print("Godrej chunks:", godrej_count)
print("JSW chunks:", jsw_count)