from form_extraction import FormParser
from base_extraction import BaseParser
from explainer_doc_extraction import ExplainerDocumentParser
from datetime import datetime

class ExtractionRunner(BaseParser):
     def __init__(self):
        super().__init__()
        self.document_index_list,self.document_index = self.load_document_index()
     
     def select_docs(self):
         # Logic to select documents for extraction
        explanation_docs = [
            d for d in self.document_index_list 
            if d["doc_role"] == "explanation"
         ]

        fact_source_docs = [
            d for d in self.document_index_list 
            if d["doc_role"] == "fact_source"
         ]

        reference_docs = [
            d for d in self.document_index_list 
            if d["doc_role"] == "reference"
         ]
        return explanation_docs, fact_source_docs, reference_docs
     
     def run(self):
        explanation_docs, fact_source_docs, reference_docs = self.select_docs()
        print("Explanation Docs:", explanation_docs)
        # Extract and parse 1099-INT form
        for doc in fact_source_docs:
            docid = doc["doc_id"]
            #print("Document ID:", docid)
            form_parser = FormParser(docid=docid)
            form_pages = form_parser.load_pages(form_parser.pdf_path)
            form_parser.save_pages_json(form_parser.doc_id, form_parser.doc_type, form_pages, form_parser.first_parse_path)
            form_schema_parsed = form_parser.schema_parse()
            #print("Schema Parsed:", form_schema_parsed.dict())
            form_parser.save_schema_parsed(form_schema_parsed, form_parser.schema_parse_path)
         
        for doc in explanation_docs:
            docid = doc["doc_id"]
            print("Document ID:", docid)
            explainer_parser = ExplainerDocumentParser(docid=docid)
            # parsing
            explainer_pages = explainer_parser.load_pages_columns(explainer_parser.pdf_path)
            # chunking
            explainer_chunks = explainer_parser.load_chunks(explainer_pages)
            print("Explainer Chunks:", explainer_chunks[0])
            # embedding and saving


if __name__ == "__main__":
    runner = ExtractionRunner()
    runner.run()