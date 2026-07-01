from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


def synthesis_node(state):
    analysis = state["analysis"]
    docs = state["retrieved_docs"]
    prompt = (
        "Na základe analýzy a zdrojových pasáží vytvor štruktúrovaný report. "
        "Zahrň: 1) Zhrnutie 2) Hlavné zistenia 3) Detailné porovnanie 4) Záver. "
        "Cituj zdrojové pasáže. "
        f"Analýza: {analysis} "
        f"Zdrojové pasáže: {docs}"
    )
    response = llm.invoke(prompt)
    return {"final_report": response.content}