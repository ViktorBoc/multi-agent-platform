import os
import tempfile

import streamlit as st

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", "")

from src.rag.document_loader import load_and_split
from src.rag.vector_store import create_vector_store
from src.agents.graph import run_agent_pipeline

st.set_page_config(page_title="Multi-Agent Research Platform", page_icon="🤖")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = 0

with st.sidebar:
    st.title("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Vyberte PDF súbory", type="pdf", accept_multiple_files=True
    )

    if st.button("Process"):
        if not uploaded_files:
            st.warning("Najprv vyberte aspoň jeden súbor.")
        elif not os.environ.get("OPENAI_API_KEY"):
            st.error("Chýba OPENAI_API_KEY v Streamlit secrets.")
        else:
            all_chunks = []
            for uploaded_file in uploaded_files:
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                try:
                    chunks = load_and_split(tmp_path)
                    all_chunks.extend(chunks)
                    st.success(f"{uploaded_file.name}: {len(chunks)} chunkov")
                finally:
                    os.remove(tmp_path)

            if all_chunks:
                if st.session_state.vector_store is None:
                    st.session_state.vector_store = create_vector_store(all_chunks)
                else:
                    st.session_state.vector_store.add_documents(all_chunks)
                st.session_state.documents_processed += len(uploaded_files)

    st.metric("Spracované dokumenty", st.session_state.documents_processed)

st.title("🤖 Multi-Agent Research Platform")
st.caption(
    "Zjednodušená standalone verzia pre Streamlit Cloud — RAG pipeline, agenti aj UI "
    "bežia v jednom procese, bez FastAPI backendu a bez samostatného ChromaDB servera."
)
st.write(
    "Nahrajte PDF dokumenty v bočnom paneli a položte otázku. Traja AI agenti "
    "spolupracujú na vyhľadaní relevantných pasáží, ich analýze a vytvorení "
    "štruktúrovaného reportu s citáciami."
)

query = st.text_input("Zadajte otázku k nahratým dokumentom...")

if st.button("Analyzovať"):
    if not query:
        st.warning("Zadajte otázku.")
    elif st.session_state.vector_store is None:
        st.warning("Najprv nahrajte a spracujte aspoň jeden dokument.")
    else:
        with st.spinner("Agenti spracúvajú vašu otázku..."):
            result = run_agent_pipeline(query, st.session_state.vector_store)

        st.subheader("Report")
        st.markdown(result["final_report"])

        with st.expander("📚 Retrieved Passages"):
            for i, doc in enumerate(result["retrieved_docs"], 1):
                st.markdown(f"**Passage {i}**")
                st.write(doc)

        with st.expander("🔍 Analysis"):
            st.write(result["analysis"])