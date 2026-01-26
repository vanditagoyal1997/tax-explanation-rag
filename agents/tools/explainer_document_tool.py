from langchain_core.tools import tool, BaseTool
from dotenv import load_dotenv
import sys
from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from .tool_format import DocumentQuery

def load_vectorstore(path: str) -> FAISS:
    """Load a FAISS vector store from the given path."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = FAISS.load_local(path,
                                    embeddings,
                                     allow_dangerous_deserialization=True
    )
    return vector_store

def retrieve_explainer_docs(query: str, k: int = 5, topic: str = "1099-INT"):
    """Retrieve relevant explainer documents for the given query."""
    vector_store = load_vectorstore("explainer_vectorstore.faiss")
    docs = vector_store.similarity_search(query,
                                           k=k,
                                           filter={
                                         "doc_type": "IRS_EXPLANATION",
                                            "doc_role": "explanation",
                                            "topic": topic
                                        
                                        }
                )
    return docs

@tool
def explainer_doc_retriever_tool(query: DocumentQuery):
    """Tool to retrieve explainer documents based on a query."""
    docs = retrieve_explainer_docs(query.question,topic= query.doc_type)
    print(f"Retrieved {len(docs)} explainer documents for question: {query.question}")
    return docs