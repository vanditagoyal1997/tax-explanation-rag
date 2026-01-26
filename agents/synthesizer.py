from .state import GraphState
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import sys
from datetime import datetime
from langchain_openai import ChatOpenAI
from .prompts.agent_prompts import SYNTHESIZER_PROMPT

sys.path.append('../')
load_dotenv()   

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
def synthesizer_node(state: GraphState) -> GraphState:
    parts = []

    # factual grounding
    if state.get("fact_results"):
        for f in state["fact_results"]:
            f = f.dict()
            parts.append(
                f"{f['field_name']} = {f['value']} (from {f['doc_type']}, page {f['source_page']})"
            )

    # explanation grounding
    if state.get("explainer_docs"):
        context = "\n".join(d.page_content for d in state["explainer_docs"])
        chain = SYNTHESIZER_PROMPT | llm
        explanation = chain.invoke({
            "question": state["question"],
            "context": context
        })

        parts.append(str(explanation.content))

    return {
        **state,
        "answer": "\n\n".join(parts)
    }
