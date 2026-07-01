from src.rag.vector_store import retrieve


def retrieval_node(state, vector_store):
    query = state["query"]
    docs = retrieve(vector_store, query)
    return {"retrieved_docs": docs}