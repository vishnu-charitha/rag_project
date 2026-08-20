from langchain_core.tools import tool

from retriever import retrieve_documents


# ==========================================
# SEARCH COMPANY DOCUMENTS TOOL
# ==========================================

@tool
def search_company_documents(query: str) -> str:
    """
    Search the Godrej and JSW sustainability
    reports for relevant information.
    """

    documents = retrieve_documents(
        query,
        k=2
    )

    if not documents:

        return "No relevant documents were found."

    results = []

    for doc in documents:

        company = doc.metadata.get(
            "company",
            "unknown"
        )

        source = doc.metadata.get(
            "source",
            "unknown"
        )

        page = doc.metadata.get(
            "page",
            "unknown"
        )

        content = doc.page_content

        results.append(
            f"""
Company: {company}
Source: {source}
Page: {page}

Content:
{content}
"""
        )

    return "\n\n".join(results)


# ==========================================
# CALCULATOR TOOL
# ==========================================

@tool
def calculator(expression: str) -> str:
    """
    Calculate a basic mathematical expression.

    Example:
    calculator("2500 * 35")
    """

    try:

        # Allow only basic calculation characters
        allowed_characters = (
            "0123456789"
            "+-*/().% "
        )

        if not all(
            character in allowed_characters
            for character in expression
        ):

            return (
                "Invalid expression. "
                "Only basic arithmetic is allowed."
            )

        result = eval(
            expression,
            {
                "__builtins__": {}
            },
            {}
        )

        return str(result)

    except Exception as e:

        return f"Calculation error: {str(e)}"