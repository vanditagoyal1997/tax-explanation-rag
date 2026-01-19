from base_extraction import BaseParser
from schema import SCHEMA_REGISTRY, ExtractedDocument
from prompt import EXTRACTION_PROMPT
import json 
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import sys
from datetime import datetime

sys.path.append('../')
print(sys.path)
load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class FormParser(BaseParser):
    def __init__(self, docid):
        super().__init__()
        self.doc_id = docid
        
        self.document_index_list,self.document_index = self.load_document_index()
        print(self.document_index)
        self.pdf_path = self.document_index[self.doc_id]["path"]
        self.doc_type = self.document_index[self.doc_id]["doc_type"]
        self.first_parse_path = self.document_index[self.doc_id]["first_parse_path"]
        self.schema_parse_path = self.document_index[self.doc_id]["schema_parse_path"]
        
    
    def load_first_parse(self):
        with open(self.first_parse_path, 'r') as f:
            first_parse = json.load(f)
        return first_parse
    
    def schema_parse(self):
        # Implement specific parsing logic for 1099-INT forms
        first_parse = self.load_first_parse()
        #print("self.schema_class:", self.schema_class)
        pages = first_parse["pages"]
        text = "\n".join(
        f"Page {p['page_number']}:\n{p['text']}"
        for p in pages
        )

        fields_model = SCHEMA_REGISTRY[self.doc_type]

        schema_json = json.dumps(
        {
            "doc_id": "string",
            "doc_type": self.doc_type,
            "fields": fields_model.schema()
        },
        indent=2
        )

        prompt = EXTRACTION_PROMPT.format(
            doc_id=self.doc_id,
            doc_type=self.doc_type,
            schema_json=schema_json,
            page_text=text
        )


        response = llm.invoke(prompt)
        content = response.content

        if "```json" in content:
            # Extract JSON from markdown code block
            json_start = content.find("```json") + 7
            json_end = content.find("```", json_start)
            json_str = content[json_start:json_end].strip()
        elif "```" in content:
            # Extract from plain code block
            json_start = content.find("```") + 3
            json_end = content.find("```", json_start)
            json_str = content[json_start:json_end].strip()
        else:
            # Assume entire response is JSON
            json_str = content

        raw_output = json.loads(json_str)

        
    
        validated_fields = fields_model(**raw_output["fields"])

        
        # # Extract JSON from the response (handles markdown code blocks)
        # content = response.content
        # 
        
        return ExtractedDocument(
        doc_id=self.doc_id,
        doc_type=self.doc_type,
        extracted_at=datetime.now(),
        fields=validated_fields.dict()
        )
    
    def save_schema_parsed(self, parsed_data, json_path):
        with open(json_path, 'w') as json_file:
            json.dump(parsed_data.dict(), json_file, indent=4, default=str)

    

if __name__ == "__main__":
    
    parser = FormParser(docid="int1099_2025")
    pages = parser.load_pages(parser.pdf_path)
    parser.save_pages_json(parser.doc_id, parser.doc_type, pages, parser.first_parse_path)
    schema_parsed = parser.schema_parse()
    print("Schema Parsed:", schema_parsed.dict())
    parser.save_schema_parsed(schema_parsed, parser.schema_parse_path)

    parser = FormParser(docid="w2_2025")
    pages = parser.load_pages(parser.pdf_path)
    parser.save_pages_json(parser.doc_id, parser.doc_type, pages, parser.first_parse_path)
    schema_parsed = parser.schema_parse()
    print("Schema Parsed:", schema_parsed.dict())
    parser.save_schema_parsed(schema_parsed, parser.schema_parse_path)
    #print(first_parse)
    #parsed_data = parser.schema_parse(Form1099INT, first_parse)
    #parser.save_json(parser.doc_id, parsed_data, "parsed_1099int.json")