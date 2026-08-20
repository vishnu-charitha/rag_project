from langgraph.graph import (
    StateGraph,
    START,
    END
)

from agent_state import AgentState

from agent_nodes import (
    decide_action,
    search_documents,
    calculate,
    direct_answer,
    generate_from_tool
)


# ==========================================
# CREATE GRAPH
# ==========================================

workflow = StateGraph(AgentState)


# ==========================================
# ADD NODES
# ==========================================

workflow.add_node(
    "decide_action",
    decide_action
)

workflow.add_node(
    "search_documents",
    search_documents
)

workflow.add_node(
    "calculate",
    calculate
)

workflow.add_node(
    "direct_answer",
    direct_answer
)

workflow.add_node(
    "generate_from_tool",
    generate_from_tool
)


# ==========================================
# START → DECISION
# ==========================================

workflow.add_edge(
    START,
    "decide_action"
)


# ==========================================
# DECISION → ACTION
# ==========================================

workflow.add_conditional_edges(
    "decide_action",

    lambda state: state["action"],

    {
        "search_documents": "search_documents",
        "calculator": "calculate",
        "direct_answer": "direct_answer"
    }
)


# ==========================================
# SEARCH → GENERATE
# ==========================================

workflow.add_edge(
    "search_documents",
    "generate_from_tool"
)


# ==========================================
# CALCULATOR → GENERATE
# ==========================================

workflow.add_edge(
    "calculate",
    "generate_from_tool"
)


# ==========================================
# GENERATE → END
# ==========================================

workflow.add_edge(
    "generate_from_tool",
    END
)


# ==========================================
# DIRECT → END
# ==========================================

workflow.add_edge(
    "direct_answer",
    END
)


# ==========================================
# COMPILE
# ==========================================

agent_app = workflow.compile()