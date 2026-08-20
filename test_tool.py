from tools import search_company_documents


result = search_company_documents.invoke(
    "What are the greenhouse gas reduction initiatives of JSW?"
)

print(result)