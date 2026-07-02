from dotenv import load_dotenv

load_dotenv()

from src.rag.document_loader import load_and_split

pdf_chunks = load_and_split("test1.pdf")
print(f"test1.pdf: {len(pdf_chunks)} chunks")
print(pdf_chunks[0].page_content[:200])

print()

docx_chunks = load_and_split("test2.docx")
print(f"test2.docx: {len(docx_chunks)} chunks")
print(docx_chunks[0].page_content[:200])

print()

png_chunks = load_and_split("test3.png")
print(f"test3.png: {len(png_chunks)} chunks")
print(png_chunks[0].page_content[:200])