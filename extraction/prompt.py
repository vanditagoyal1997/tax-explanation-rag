EXTRACTION_PROMPT = """
You are extracting structured facts from a tax document.

You MUST follow these rules:
- Only extract values that are explicitly present in the document text.
- If a value is missing, return null.
- Do NOT infer, calculate, normalize, or reinterpret values.
- Every extracted value MUST include the page number it came from.
- Page numbers must match the page numbers in the provided text.
- Use the provided doc_id exactly as given.
- Return ONLY valid JSON that strictly matches the provided schema.
- Do NOT add, remove, or rename fields.

Document metadata:
- doc_id: {doc_id}
- doc_type: {doc_type}

Schema (JSON Schema):
{schema_json}

Document text (page-level, prefixed with page numbers):
{page_text}
"""
