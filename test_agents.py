from src.rag.document_loader import load_and_split
from src.rag.vector_store import create_vector_store
from src.agents.graph import run_agent_pipeline

chunks = load_and_split("test.pdf")
vector_store = create_vector_store(chunks)

query = "Summarize the key findings of this document"
result = run_agent_pipeline(query, vector_store)

print("=== Retrieved Docs ===")
for i, doc in enumerate(result["retrieved_docs"], 1):
    print(f"--- Doc {i} ---")
    print(doc)
    print()

print("=== Analysis ===")
print(result["analysis"])
print()

print("=== Final Report ===")
print(result["final_report"])