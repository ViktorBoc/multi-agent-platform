import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Multi-Agent Research Platform", page_icon="🤖")

if "documents_uploaded" not in st.session_state:
    st.session_state.documents_uploaded = 0

with st.sidebar:
    st.title("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload Documents (PDF, Word, PowerPoint, Excel, HTML, CSV, Images)",
        type=[
            "pdf", "docx", "pptx", "xlsx", "html", "csv", "json", "xml",
            "jpg", "jpeg", "png", "gif", "bmp", "tiff",
        ],
        accept_multiple_files=True,
    )

    if st.button("Upload"):
        if not uploaded_files:
            st.warning("Najprv vyberte aspoň jeden súbor.")
        else:
            for uploaded_file in uploaded_files:
                try:
                    files = {
                        "file": (uploaded_file.name, uploaded_file.getvalue())
                    }
                    response = requests.post(f"{API_URL}/upload", files=files)
                    if response.status_code == 200:
                        chunks = response.json().get("chunks_loaded", 0)
                        st.success(f"{uploaded_file.name}: nahraných {chunks} chunkov")
                        st.session_state.documents_uploaded += 1
                    else:
                        st.error(f"{uploaded_file.name}: chyba API ({response.status_code})")
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Nepodarilo sa pripojiť k API. Beží backend na http://localhost:8000?"
                    )
                    break

    st.metric("Nahraté dokumenty", st.session_state.documents_uploaded)

st.title("🤖 Multi-Agent Research Platform")
st.write(
    "Nahrajte PDF dokumenty v bočnom paneli a položte otázku. Traja AI agenti "
    "spolupracujú na vyhľadaní relevantných pasáží, ich analýze a vytvorení "
    "štruktúrovaného reportu s citáciami."
)

query = st.text_input("Zadajte otázku k nahratým dokumentom...")

if st.button("Analyzovať"):
    if not query:
        st.warning("Zadajte otázku.")
    else:
        with st.spinner("Agenti spracúvajú vašu otázku..."):
            try:
                response = requests.post(f"{API_URL}/query", json={"query": query})
                if response.status_code == 200:
                    result = response.json()

                    st.subheader("Report")
                    st.markdown(result["final_report"])

                    with st.expander("📚 Retrieved Passages"):
                        for i, doc in enumerate(result["retrieved_docs"], 1):
                            st.markdown(f"**Passage {i}**")
                            st.write(doc)

                    with st.expander("🔍 Analysis"):
                        st.write(result["analysis"])
                elif response.status_code == 400:
                    st.error(response.json().get("detail", "Najprv nahrajte dokumenty."))
                else:
                    st.error(f"API chyba: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Nepodarilo sa pripojiť k API. Uistite sa, že backend beží na "
                    "http://localhost:8000."
                )
