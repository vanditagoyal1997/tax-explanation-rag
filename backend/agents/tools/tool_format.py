from pydantic import BaseModel
from typing import Optional, Union

class DocumentQuery(BaseModel):
    question: str
    doc_type: Optional[str] = None

class FactResult(BaseModel):
    doc_id: str
    doc_type: str
    field_name: str
    value: Optional[Union[str, float, int]]
    source_page: Optional[int]



FIELD_SYNONYMS = {
    "interest_income": [
        "interest income",
        "interest earned",
        "bank interest",
        "1099 interest"
    ],
    "wages": [
        "wages",
        "salary",
        "income from job",
        "earned income"
    ],
    "federal_withholding": [
        "federal tax withheld",
        "withholding",
        "federal withholding"
    ],
    "payer_name": [
        "payer",
        "bank name",
        "who paid",
        "institution"
    ],
    "employer_name": [
        "employer",
        "company",
        "who paid me"
    ],
    "tax_year": [
        "tax year",
        "year",
        "for which year"
    ]
}

