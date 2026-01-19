import pdfplumber
from abc import abstractmethod, ABC
import json

class BaseParser(ABC):
    def __init__(self):
        self.document_index_path = "document_index.json"

    def load_document_index(self):
        document_index = {}
        with open(self.document_index_path, 'r') as f:
            document_index_list = json.load(f)
        document_index = {doc["doc_id"]: doc for doc in document_index_list} 
        return document_index_list, document_index
    
    def load_pages(self, pdf_path):
        pages = []

        with pdfplumber.open(pdf_path) as pdf:
            for i,page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    pages.append({
                        "page_number": i + 1,
                        "text": page_text or ""
                })

        return pages
    
    def save_pages_json(self,docid, doc_type, pages, json_path):
        data = {"doc_id":docid,"doc_type":doc_type,"pages": pages}
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    
    
if __name__ == "__main__":
    parser = BaseParser()
    pages_int1099 = parser.load_pages("../Data/INT1099_form.pdf")
    for page in pages_int1099:
        print(f"Page {page['page_number']}:\n{page['text']}\n")
    