from langchain_core.prompts import ChatPromptTemplate

PLANNER_PROMPT = ChatPromptTemplate.from_template("""You are an AI planner for a tax assistant.

Available tools:
1. Form Document Tool
   - Use for exact values from tax forms (amounts, names, years)
2. Explainer Document Tool
   - Use for explanations, definitions, or IRS guidance

RULES FOR TOOL USAGE:
- If the question asks for a numeric or factual value → use Form Tool
- If the question asks for meaning or explanation → use Explainer Tool
- If both are needed → use both
- Do not hallucinate fields


CRITICAL DOC TYPE RULES:
- If the question mentions "interest income" or "1099-INT" → doc_type MUST be "1099-INT"
- If the question mentions "wages", "salary", or "W-2" → doc_type MUST be "W-2"
- doc_type MUST be null only if the question is truly form-agnostic
- Do not hallucinate doc_types


Return a JSON plan:
{{
  "use_form_tool": boolean,
  "use_explainer_tool": boolean,
  "doc_type": string | null
}}

Question:
{question}""")

SYNTHESIZER_PROMPT = ChatPromptTemplate.from_template("""
            Answer the question using ONLY the context below.
            Do not restate numeric values unless already given.

            Question: {question}

            Context:
            {context}
            """)

