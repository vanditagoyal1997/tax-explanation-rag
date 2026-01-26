from langchain_core.tools import tool, BaseTool
from typing import Optional, Union, List
from extraction.schema import SCHEMA_REGISTRY,ExtractedDocument
from .tool_format import DocumentQuery, FIELD_SYNONYMS, FactResult
from .helper import load_parsed_docs

PARSED_FORM_DOCUMENTS = load_parsed_docs("schema_parsed_doc")

def map_question_to_field(
    question: str,
    doc_type: str
) -> str | None:
    q = question.lower()

    schema_cls = SCHEMA_REGISTRY.get(doc_type)
    print("Mapping question to field for doc_type:", doc_type)
    if not schema_cls:
        return None

    valid_fields = schema_cls.model_fields.keys()

    for field in valid_fields:
        synonyms = FIELD_SYNONYMS.get(field, [])
        for phrase in synonyms:
            if phrase in q:
                return field

    return None

def lookup_structured_fact(
    parsed_docs: List[ExtractedDocument],
    field_name: str,
    doc_type: Optional[str] = None
) -> List[FactResult]:
    """
    Deterministically retrieve a structured field from parsed schema documents.
    """
    print("Looking up field:", field_name, "in doc_type:", doc_type)
    print("Parsed docs count:", len(parsed_docs))
    results: List[FactResult] = []

    for doc in parsed_docs:
        if doc_type and doc.doc_type != doc_type:
            continue

        schema_cls = SCHEMA_REGISTRY.get(doc.doc_type)
        if not schema_cls:
            continue  # unknown form, skip safely

        fields_obj = doc.fields
        print("fields_obj:", fields_obj)

        if field_name not in fields_obj:
            print("Field", field_name, "not found in document fields.")
            continue

        field = fields_obj[field_name]
        print("Found field:", field_name, "with value:", field.value if field else None)

        if field is None or field.value is None:
            continue

        results.append(
            FactResult(
                doc_id=doc.doc_id,
                doc_type=doc.doc_type,
                field_name=field_name,
                value=field.value,
                source_page=field.source_page
            )
        )

    return results


@tool
def form_doc_retriever_tool(query: DocumentQuery) -> str:
    """Tool to retrieve facts (fields from a form) based on a query."""
    field_name = map_question_to_field(
        question=query.question,
        doc_type=query.doc_type
    )
    print("Mapped question to field name:", field_name)
    if not field_name:
        return []
    

    return lookup_structured_fact(
        parsed_docs=PARSED_FORM_DOCUMENTS,
        field_name=field_name,
        doc_type=query.doc_type
    )
