from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

from tools import search_company_documents,calculator
from agent_state import AgentState


# ==========================================
# LOAD LOCAL MODEL
# ==========================================

model_name = "google/flan-t5-base"

print("Loading local agent model...")

tokenizer = AutoTokenizer.from_pretrained(
    model_name
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name
)

print("Agent model loaded!")


# ==========================================
# AGENT DECISION NODE
# ==========================================

def decide_action(state: AgentState):

    question = state["question"]

    print("\n--- AGENT DECISION NODE ---")

    question_lower = question.lower()

    # --------------------------------------
    # CALCULATOR KEYWORDS
    # --------------------------------------

    calculator_keywords = [
        "calculate",
        "what is",
        "how much is",
        "multiply",
        "divide",
        "addition",
        "subtraction",
        "percentage",
        "%",
        "*",
        "/",
        "+",
        "-"
    ]

    # --------------------------------------
    # RAG KEYWORDS
    # --------------------------------------

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

    # --------------------------------------
    # CALCULATOR DECISION
    # --------------------------------------

    # Basic arithmetic expressions
    has_math_operator = any(
        operator in question
        for operator in ["+", "-", "*", "/"]
    )

    has_number = any(
        character.isdigit()
        for character in question
    )

    if has_number and has_math_operator:

        print(
            "Agent selected: calculator"
        )

        return {
            "action": "calculator"
        }

    for keyword in calculator_keywords:

        if keyword in question_lower:

            # Avoid routing company questions just
            # because they contain "what is"
            if any(
                word in question_lower
                for word in rag_keywords
            ):

                break

            print(
                "Agent selected: calculator"
            )

            return {
                "action": "calculator"
            }

    # --------------------------------------
    # SEARCH DOCUMENTS DECISION
    # --------------------------------------

    for keyword in rag_keywords:

        if keyword in question_lower:

            print(
                "Agent selected: search_documents"
            )

            return {
                "action": "search_documents"
            }

    # --------------------------------------
    # DIRECT ANSWER
    # --------------------------------------

    print(
        "Agent selected: direct_answer"
    )

    return {
        "action": "direct_answer"
    }

# ==========================================
# SEARCH DOCUMENTS TOOL NODE
# ==========================================

def search_documents(state: AgentState):

    question = state["question"]

    print("\n--- SEARCH DOCUMENTS TOOL ---")

    try:

        result = search_company_documents.invoke(
            question
        )

        return {
            "tool_result": result
        }

    except Exception as e:

        print(
            "Tool error:",
            str(e)
        )

        return {
            "tool_result": (
                "Unable to retrieve documents."
            )
        }
    # ==========================================
# CALCULATOR TOOL NODE
# ==========================================

def calculate(state: AgentState):

    question = state["question"]

    print("\n--- CALCULATOR TOOL ---")

    # Extract the mathematical expression
    expression = question

    # Simple extraction for natural language
    replacements = {
        "what is": "",
        "calculate": "",
        "how much is": "",
        "multiply": "*",
        "divided by": "/",
        "divide by": "/",
    }

    expression = expression.lower()

    for old, new in replacements.items():

        expression = expression.replace(
            old,
            new
        )

    expression = expression.strip()

    print(
        "Expression:",
        expression
    )

    result = calculator.invoke(
        expression
    )

    print(
        "Calculator result:",
        result
    )

    return {
        "tool_result": result
    }


# ==========================================
# DIRECT ANSWER NODE
# ==========================================

def direct_answer(state: AgentState):

    question = state["question"]

    print("\n--- DIRECT ANSWER NODE ---")

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question directly and clearly.

Question:
{question}

Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=False
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    ).strip()

    return {
        "answer": answer
    }


# ==========================================
# GENERATE ANSWER FROM TOOL RESULT
# ==========================================

def generate_from_tool(state: AgentState):

    question = state["question"]

    tool_result = state["tool_result"]

    print("\n--- AGENT GENERATION NODE ---")

    prompt = f"""
You are an expert assistant answering questions
from company sustainability reports.

Answer the user's question using ONLY the
retrieved information below.

Question:
{question}

Retrieved Information:
{tool_result}

Instructions:
- Give a clear and direct answer.
- Use bullet points when appropriate.
- Keep important company names.
- Keep important numbers, dates, targets, and percentages.
- Do not invent information.
- Do not copy irrelevant table headings.
- Do not repeat information.
- If the retrieved information does not contain
  the answer, say:
  "I could not find the answer in the provided documents."

Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        num_beams=4,
        do_sample=False,
        repetition_penalty=1.2
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    ).strip()

    return {
        "answer": answer
    }