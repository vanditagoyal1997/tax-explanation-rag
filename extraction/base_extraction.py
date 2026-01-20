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
    
    def split_columns(self, words, page_width):
        if not words:
            return [], []

        left_col = []
        right_col = []

        for w in words:
            # Bias wide / centered text to left column
            if w["x0"] < page_width * 0.48:
                left_col.append(w)
            else:
                right_col.append(w)

        return left_col, right_col

    
    def words_to_lines(self, words, line_threshold=3):
        lines = []
        current_line = []
        last_top = None

        for w in words:
            if last_top is None or abs(w["top"] - last_top) <= line_threshold:
                current_line.append(w["text"])
            else:
                lines.append(" ".join(current_line))
                current_line = [w["text"]]
            last_top = w["top"]

        if current_line:
            lines.append(" ".join(current_line))

        return "\n".join(lines)


    def load_pages_columns(self, pdf_path):
        pages = []

        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                words = page.extract_words(use_text_flow=False)

                left_col, right_col = self.split_columns(words, page.width)

                left_sorted = sorted(left_col, key=lambda w: (w["top"], w["x0"]))
                right_sorted = sorted(right_col, key=lambda w: (w["top"], w["x0"]))

                left_text = self.words_to_lines(left_sorted)
                right_text = self.words_to_lines(right_sorted)

                pages.append({
                "page_number": page_num,
                "text": left_text + "\n\n" + right_text
                })

        return pages

        


    
    def load_sections(self, pdf_path):
        # Placeholder for section loading logic
        pass
    
    def save_pages_json(self,docid, doc_type, pages, json_path):
        data = {"doc_id":docid,"doc_type":doc_type,"pages": pages}
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    
    
if __name__ == "__main__":
    parser = BaseParser()
    pages_int1099 = parser.load_pages("../Data/INT1099_form.pdf")
    for page in pages_int1099:
        print(f"Page {page['page_number']}:\n{page['text']}\n")
    