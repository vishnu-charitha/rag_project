from langgraph.graph import StateGraph, START, END

from state import RAGState

from nodes import (
    router,
    retrieve,
    grade_documents,
    rewrite_query,
    generate,
    direct_answer
)


# ==========================================
# CREATE GRAPH
# ==========================================

workflow = StateGraph(RAGState)


# ==========================================
# ADD NODES
# ==========================================

workflow.add_node("router", router)

workflow.add_node("retrieve", retrieve)

workflow.add_node(
    "grade_documents",
    grade_documents
)

workflow.add_node(
    "rewrite_query",
    rewrite_query
)

workflow.add_node(
    "generate",
    generate
)

workflow.add_node(
    "direct_answer",
    direct_answer
)


# ==========================================
# START → ROUTER
# ==========================================

workflow.add_edge(
    START,
    "router"
)


# ==========================================
# ROUTER → RAG / DIRECT
# ==========================================

workflow.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {
        "rag": "retrieve",
        "direct": "direct_answer"
    }
)


# ==========================================
# RETRIEVE → GRADE
# ==========================================

workflow.add_edge(
    "retrieve",
    "grade_documents"
)


# ==========================================
# GRADE → GENERATE / REWRITE
# ==========================================

workflow.add_conditional_edges(
    "grade_documents",
    lambda state: state["document_grade"],
    {
        "relevant": "generate",
        "not_relevant": "rewrite_query"
    }
)


# ==========================================
# REWRITE → CONDITIONAL ROUTING
# ==========================================

workflow.add_conditional_edges(
    "rewrite_query",
    lambda state: (
        "retry"
        if state.get("rewrite_count", 0) < 2
        else "stop"
    ),
    {
        "retry": "retrieve",
        "stop": END
    }
)


# ==========================================
# GENERATE → END
# ==========================================

workflow.add_edge(
    "generate",
    END
)


# ==========================================
# DIRECT ANSWER → END
# ==========================================

workflow.add_edge(
    "direct_answer",
    END
)


# ==========================================
# COMPILE
# ==========================================

app = workflow.compile()