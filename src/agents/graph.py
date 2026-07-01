from functools import partial

from langgraph.graph import StateGraph, START, END

from src.agents.state import AgentState
from src.agents.retrieval_agent import retrieval_node
from src.agents.analysis_agent import analysis_node
from src.agents.synthesis_agent import synthesis_node


def build_graph(vector_store):
    graph = StateGraph(AgentState)

    graph.add_node("retrieve", partial(retrieval_node, vector_store=vector_store))
    graph.add_node("analyze", analysis_node)
    graph.add_node("synthesize", synthesis_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "analyze")
    graph.add_edge("analyze", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile()


def run_agent_pipeline(query, vector_store):
    compiled_graph = build_graph(vector_store)
    initial_state = {
        "query": query,
        "retrieved_docs": [],
        "analysis": "",
        "final_report": "",
    }
    return compiled_graph.invoke(initial_state)