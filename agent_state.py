from typing import TypedDict


class AgentState(TypedDict):
    question: str
    action: str
    tool_result: str
    answer: str