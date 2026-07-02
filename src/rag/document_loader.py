from langchain_text_splitters import RecursiveCharacterTextSplitter
from markitdown import MarkItDown
from openai import OpenAI


def load_and_split(file_path):
    md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o-mini")
    result = md.convert(file_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents(
        [result.text_content], metadatas=[{"source": file_path}]
    )

    return chunks