from base_extraction import BaseParser
import json 
import re
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import sys
from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS



sys.path.append('../')
#print(sys.path)
load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class ExplainerDocumentParser(BaseParser):
    def __init__(self, docid):
        super().__init__()
        self.doc_id = docid
        
        self.document_index_list,self.document_index = self.load_document_index()
        #print(self.document_index)
        self.pdf_path = self.document_index[self.doc_id]["path"]
        self.doc_type = self.document_index[self.doc_id]["doc_type"]
        self.doc_role = self.document_index[self.doc_id]["doc_role"]
        self.topic = self.document_index[self.doc_id].get("topic", "General")

    
    def strip_boilerplate(self,text):
        blacklist = [
        "Draft Ok to Print",
        "MUST be removed before printing",
        "Userid:",
        "Pt. size:",
        "Department of the Treasury",
        "Internal Revenue Service"
    ]

        lines = text.splitlines()
        cleaned = [
            line.strip()
            for line in lines
            if line.strip() and not any(b in line for b in blacklist)
        ]

        return "\n".join(cleaned)
    
    def load_sections(self, text):
        SECTION_HEADER_REGEX = re.compile(
        r"^(?:\d+\.\s+)?[A-Z][A-Za-z\s\-]{5,}$"
        )
        lines = text.splitlines()
        sections = []

        current_title = "INTRO"
        current_lines = []

        for line in lines:
            if SECTION_HEADER_REGEX.match(line):
                if current_lines:
                    sections.append({
                    "section_title": current_title,
                    "text": "\n".join(current_lines)
                    })
                current_title = line.strip()
                current_lines = []
            else:
                current_lines.append(line)

        if current_lines:
            sections.append({
            "section_title": current_title,
            "text": "\n".join(current_lines)
            })

        return sections
    
    def chunk_section(self,text,max_tokens=450,overlap_tokens=50):
        words = text.split()
        chunks = []

        step = int((max_tokens - overlap_tokens) / 1.3)
        size = int(max_tokens / 1.3)

        for i in range(0, len(words), step):
            chunk = words[i:i + size]
            chunks.append(" ".join(chunk))

        return chunks
    
    def load_chunks(self, pages):
        all_chunks = []
        for page in pages:
            page_number = page["page_number"]
            text = self.strip_boilerplate(page["text"])
            sections = self.load_sections(text)
            for section in sections:
                section_title = section["section_title"]
                section_text = section["text"]
                chunks = self.chunk_section(section_text)
                for idx, chunk in enumerate(chunks):
                    all_chunks.append({
                    "doc_id": self.doc_id,
                    "doc_role": self.doc_role,
                    "doc_type": self.doc_type,
                    "topic": self.topic,
                    "page_number": page_number,
                    "section_title": section_title,
                    "chunk_index": idx + 1,
                    "text": chunk
                    })
        return all_chunks
    
    def prepare_corpus(self,chunks):
        texts = [c["text"] for c in chunks]
        metadatas = [
            {
            "doc_id": c["doc_id"],
            "doc_role": c["doc_role"],  
            "doc_type": c["doc_type"],   
            "topic": c["topic"],               
            "section_title": c["section_title"],
            "page_number": c["page_number"],
            "chunk_index": c["chunk_index"]
            }
            for c in chunks
        ]
        return texts, metadatas
    
    def build_vectorstore(self,chunks):
        texts, metadatas = self.prepare_corpus(chunks)

        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large"
        )

        vectorstore = FAISS.from_texts(
            texts=texts,
            metadatas=metadatas,
            embedding=embeddings
        )

        return vectorstore
    
    def save_vectorstore(self,vectorstore, filepath):
        vectorstore.save_local(filepath)


    
    




        