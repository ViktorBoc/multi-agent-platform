from src.rag.document_loader import load_and_split
from src.rag.vector_store import create_vector_store, retrieve

chunks = load_and_split("test.pdf")
print(f"Loaded {len(chunks)} chunks")

vector_store = create_vector_store(chunks)

query = "What is the main topic of this document?"
results = retrieve(vector_store, query, k=5)

print(f"\nQuery: {query}\n")
for i, result in enumerate(results, 1):
    print(f"--- Result {i} ---")
    print(result)
    print()