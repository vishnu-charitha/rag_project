from retriever import retrieve_documents
from state import RAGState

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)


# ==========================================
# LOAD MODEL
# ==========================================

model_name = "google/flan-t5-base"

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print("Model loaded successfully!")


# ==========================================
# ROUTER NODE
# ==========================================

def router(state: RAGState):

    question = state["question"]

    print("\n--- ROUTER NODE ---")

    question_lower = question.lower()

    # Keywords related to your company reports
    rag_keywords = [
        "jsw",
        "godrej",
        "sustainability",
        "sustainable",
        "esg",
        "environment",
        "environmental",
        "greenhouse gas",
        "carbon",
        "emission",
        "emissions",
        "co2",
        "climate",
        "net zero",
        "energy",
        "waste",
        "water",
        "biodiversity",
        "annual report",
        "company report",
        "decarbonisation",
        "decarbonization",
        "raw material",
        "scrap"
    ]

    # Check if question requires RAG
    for keyword in rag_keywords:

        if keyword in question_lower:

            print("Keyword matched:", keyword)
            print("Final route: rag")

            return {
                "route": "rag"
            }

    # Otherwise use direct answer
    print("No RAG keyword matched.")
    print("Final route: direct")

    return {
        "route": "direct"
    }


# ==========================================
# RETRIEVE NODE
# ==========================================

def retrieve(state: RAGState):

    question = state["question"]

    print("\n--- RETRIEVE NODE ---")

    # Retrieve top 2 documents
    documents = retrieve_documents(
        question,
        k=2
    )

    print(
        f"Retrieved {len(documents)} documents"
    )

    # Display retrieved documents
    for i, doc in enumerate(
        documents,
        start=1
    ):

        print(
            f"\n--- RETRIEVED DOCUMENT {i} ---"
        )

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

    return {
        "documents": documents
    }


# ==========================================
# LLM DOCUMENT GRADING NODE
# ==========================================

def grade_documents(state: RAGState):

    question = state["question"]
    documents = state["documents"]

    print("\n--- GRADE DOCUMENTS NODE ---")

    relevant_documents = []

    for i, doc in enumerate(
        documents,
        start=1
    ):

        document_text = doc.page_content

        prompt = f"""
You are a document relevance grader.

Determine whether the document contains information
that can help answer the question.

Question:
{question}

Document:
{document_text}

Return ONLY one word:
yes
or
no
"""

        # Tokenize
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )

        # Generate grade
        outputs = model.generate(
            **inputs,
            max_new_tokens=5,
            do_sample=False
        )

        # Decode model output
        grade = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        # Normalize output
        grade = grade.strip().lower()

        print(
            f"Document {i} raw grade: {repr(grade)}"
        )

        # Accept YES as relevant
        if (
            grade == "yes"
            or grade.startswith("yes")
        ):

            relevant_documents.append(doc)

            print(
                f"Document {i} accepted as relevant."
            )

        else:

            print(
                f"Document {i} rejected as not relevant."
            )

    print(
        f"Relevant documents found: "
        f"{len(relevant_documents)}"
    )

    # At least one relevant document
    if relevant_documents:

        print(
            "Document grade: relevant"
        )

        return {
            "documents": relevant_documents,
            "document_grade": "relevant"
        }

    # No relevant documents
    print(
        "Document grade: not_relevant"
    )

    return {
        "documents": [],
        "document_grade": "not_relevant"
    }


# ==========================================
# QUERY REWRITE NODE
# ==========================================

def rewrite_query(state: RAGState):

    question = state["question"]

    rewrite_count = state.get(
        "rewrite_count",
        0
    )

    print(
        "\n--- REWRITE QUERY NODE ---"
    )

    rewrite_count += 1

    # Prevent infinite rewriting
    if rewrite_count > 2:

        print(
            "Maximum rewrite attempts reached."
        )

        return {
            "question": question,
            "rewrite_count": rewrite_count
        }

    prompt = f"""
You are a query rewriting assistant.

Rewrite the user's question so that it is clearer,
more specific, and better suited for searching a
company sustainability report.

IMPORTANT:
- Preserve the company name exactly if one exists.
- Do not remove "Godrej" or "JSW".
- Preserve the original meaning.
- Make the query useful for semantic document retrieval.
- Return ONLY the rewritten question.

Original question:
{question}

Rewritten question:
"""

    # Tokenize
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # Generate rewritten query
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=False
    )

    # Decode
    rewritten_question = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    ).strip()

    print(
        "Original question:",
        question
    )

    print(
        "Rewritten question:",
        rewritten_question
    )

    return {
        "question": rewritten_question,
        "rewrite_count": rewrite_count
    }


# ==========================================
# GENERATE NODE
# ==========================================

def generate(state: RAGState):

    question = state["question"]

    documents = state["documents"]

    print(
        "\n--- GENERATE NODE ---"
    )

    # Combine retrieved documents
    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    prompt = f"""
You are an expert assistant answering questions
from company sustainability reports.

Answer the user's question using ONLY the information
contained in the context.

IMPORTANT:
- Do not copy tables directly.
- Extract the actual initiatives, targets,
  technologies, actions, and outcomes.
- Summarize the information in clear bullet points.
- Keep important names, numbers, dates, and percentages.
- Do not invent information.
- If the context contains a target, include the target.
- If the context contains specific initiatives, list them.
- Ignore irrelevant table headings and column names.
- Do not repeat the same information.
- If the answer is not available in the context, say:
  "I could not find the answer in the provided documents."

Question:
{question}

Context:
{context}

Provide a concise answer with bullet points.

Answer:
"""

    # Tokenize prompt
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    # Generate answer
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        num_beams=4,
        do_sample=False,
        repetition_penalty=1.2
    )

    # Decode answer
    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return {
        "answer": answer
    }


# ==========================================
# DIRECT ANSWER NODE
# ==========================================

def direct_answer(state: RAGState):

    question = state["question"]

    print(
        "\n--- DIRECT ANSWER NODE ---"
    )

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question directly and clearly.

Question:
{question}

Answer:
"""

    # Tokenize
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # Generate answer
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=False
    )

    # Decode answer
    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return {
        "answer": answer
    }