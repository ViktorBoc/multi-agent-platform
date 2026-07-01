from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


def analysis_node(state):
    docs = state["retrieved_docs"]
    prompt = (
        "Na základe nasledujúcich pasáží z dokumentov, analyzuj hlavné témy, "
        "identifikuj vzory a porovnaj rôzne perspektívy. "
        f"Pasáže: {docs}"
    )
    response = llm.invoke(prompt)
    return {"analysis": response.content}