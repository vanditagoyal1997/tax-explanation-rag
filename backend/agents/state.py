from typing import TypedDict, Optional, List, Dict, Any
from langchain_core.documents import Document


class ToolPlan(TypedDict):
    use_form_tool: bool
    use_explainer_tool: bool
    doc_type: Optional[str]
    field_name: Optional[str]
    justification: str  # reasoning behind the plan

class GraphState(TypedDict):
    question: str

    # planner output
    plan: Optional[ToolPlan]

    # executor outputs
    fact_results: Optional[list]
    explainer_docs: Optional[List[Document]]

    # final answer
    answer: Optional[str]

    # tracing the reasoning steps
    trace: List[Dict[str, Any]]

