from pydantic import BaseModel
from typing import Optional,Union
from datetime import datetime

class ExtractedField(BaseModel):
    value: Optional[Union[str, float, int]]
    source_page: Optional[int]


class Form1099INTFields(BaseModel):
    interest_income: Optional[ExtractedField]
    payer_name: Optional[ExtractedField]
    tax_year: Optional[ExtractedField]


class FormW2Fields(BaseModel):
    wages: Optional[ExtractedField]
    federal_withholding: Optional[ExtractedField]
    employer_name: Optional[ExtractedField]
    tax_year: Optional[ExtractedField]


class ExtractedDocument(BaseModel):
    doc_id: str
    doc_type: str
    extracted_at: datetime
    fields: dict

SCHEMA_REGISTRY = {
    "1099-INT": Form1099INTFields,
    "W-2": FormW2Fields
}

