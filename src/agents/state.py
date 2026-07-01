from typing import TypedDict


class AgentState(TypedDict):
    query: str
    retrieved_docs: list[str]
    analysis: str
    final_report: str