import os

import chromadb
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-small"
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = 8000


def create_vector_store(documents):
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    vector_store = Chroma.from_documents(documents=documents, embedding=embeddings, client=client)
    return vector_store


def retrieve(vector_store, query, k=5):
    results = vector_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]