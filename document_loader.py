from langchain_community.document_loaders import PyPDFLoader


# ==========================================
# LOAD GODREJ PDF
# ==========================================

godrej_loader = PyPDFLoader("data/godrej.pdf")

godrej_documents = godrej_loader.load()

# Add company metadata
for document in godrej_documents:

    document.metadata["company"] = "godrej"


# ==========================================
# LOAD JSW PDF
# ==========================================

jsw_loader = PyPDFLoader("data/jsw.pdf")

jsw_documents = jsw_loader.load()

# Add company metadata
for document in jsw_documents:

    document.metadata["company"] = "jsw"


# ==========================================
# COMBINE DOCUMENTS
# ==========================================

documents = godrej_documents + jsw_documents


print("Godrej pages:", len(godrej_documents))
print("JSW pages:", len(jsw_documents))
print("Total pages:", len(documents))