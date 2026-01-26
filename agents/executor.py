from .state import GraphState
from .tools.form_document_tool import form_doc_retriever_tool
from .tools.explainer_document_tool import explainer_doc_retriever_tool
from .tools.tool_format import DocumentQuery

def executor_node(state: GraphState) -> GraphState:
    plan = state["plan"]
    trace = state.get("trace", [])


    fact_results = None
    explainer_docs = None

    query = DocumentQuery(
        question=state["question"],
        doc_type=plan.get("doc_type")
    )


    if plan["use_form_tool"]:
        print("Invoking form document retriever tool...")
        fact_results = form_doc_retriever_tool.invoke({
            "query": query
        })
        trace.append({
            "node": "executor",
            "tool": "form_doc_retriever",
            "input": query.model_dump_json(),
            "output_summary": f"{len(fact_results)} fact(s) returned"
        })

    if plan["use_explainer_tool"]:
        print("Invoking explainer document retriever tool...")
        explainer_docs = explainer_doc_retriever_tool.invoke({
            "query": query
        })
        trace.append({
            "node": "executor",
            "tool": "explainer_doc_retriever",
            "input": query.model_dump_json(),
            "output_summary": f"{len(explainer_docs)} document chunk(s) returned"
        })


    return {
        **state,
        "fact_results": fact_results,
        "explainer_docs": explainer_docs,
        "trace": trace
    }
