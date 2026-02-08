from extraction.schema import SCHEMA_REGISTRY,ExtractedDocument, ExtractedField
from pathlib import Path
import json
from datetime import datetime
def load_parsed_docs(parsed_dir: str) -> list[ExtractedDocument]:
    parsed_docs = []

    for path in Path(parsed_dir).glob("*.json"):
        with open(path, "r") as f:
            raw = json.load(f)

        doc_type = raw["doc_type"]
        schema_cls = SCHEMA_REGISTRY.get(doc_type)

        if not schema_cls:
            continue  # unknown form, skip safely

        # Convert raw field dicts to ExtractedField objects
        fields_dict = {}
        for field_name, field_data in raw["fields"].items():
            if isinstance(field_data, dict):
                fields_dict[field_name] = ExtractedField(**field_data)
            else:
                fields_dict[field_name] = field_data

        extracted_doc = ExtractedDocument(
            doc_id=raw["doc_id"],
            doc_type=doc_type,
            extracted_at=datetime.fromisoformat(raw["extracted_at"]),
            fields=fields_dict
        )

        parsed_docs.append(extracted_doc)

    return parsed_docs