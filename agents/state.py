from typing import TypedDict, Optional, List, Literal
from langchain_core.documents import Document


class ToolPlan(TypedDict):
    use_form_tool: bool
    use_explainer_tool: bool
    doc_type: Optional[str]
    field_name: Optional[str]

class GraphState(TypedDict):
    question: str

    # planner output
    plan: Optional[ToolPlan]

    # executor outputs
    fact_results: Optional[list]
    explainer_docs: Optional[List[Document]]

    # final answer
    answer: Optional[str]
