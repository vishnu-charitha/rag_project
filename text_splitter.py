from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import documents


# ==========================================
# TEXT SPLITTER
# ==========================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


# Split documents into chunks
chunks = text_splitter.split_documents(documents)


print("Total chunks:", len(chunks))


# ==========================================
# COUNT CHUNKS BY COMPANY
# ==========================================

godrej_count = 0
jsw_count = 0


for chunk in chunks:

    company = chunk.metadata.get("company")

    if company == "godrej":
        godrej_count += 1

    elif company == "jsw":
        jsw_count += 1


print("Godrej chunks:", godrej_count)
print("JSW chunks:", jsw_count)