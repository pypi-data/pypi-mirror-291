import os
import pandas as pd
import docx2txt
from langchain.schema import Document as LangChainDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2
import streamlit as st

class DataLoader:
    def __init__(self, filepath_or_url, user_agent=None):
        self.filepath_or_url = filepath_or_url
        self.user_agent = user_agent
    
    def load_document(self):
        file_extension = os.path.splitext(self.filepath_or_url)[1].lower()
        
        if file_extension == '.pdf':
            documents = self._load_pdf()
        elif file_extension == '.txt':
            with open(self.filepath_or_url, 'r', encoding='utf-8') as file:
                text = file.read()
            documents = [LangChainDocument(page_content=text, metadata={"source": self.filepath_or_url})]
        elif file_extension in ['.docx', '.doc']:
            text = docx2txt.process(self.filepath_or_url)
            documents = [LangChainDocument(page_content=text, metadata={"source": self.filepath_or_url})]
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(self.filepath_or_url)
            documents = [LangChainDocument(page_content=df.to_string(), metadata={"source": self.filepath_or_url})]
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        return documents

    def _load_pdf(self):
        with open(self.filepath_or_url, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return [LangChainDocument(page_content=text, metadata={"source": self.filepath_or_url})]

    def chunk_document(self, documents, chunk_size=1024, chunk_overlap=80):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        return text_splitter.split_documents(documents)

    def process_document(self, chunk_size=1024, chunk_overlap=80):
        documents = self.load_document()
        if len(documents) == 1 and (self.filepath_or_url.endswith(('.xlsx', '.xls'))):
            chunks = documents  
        else:
            chunks = self.chunk_document(documents, chunk_size, chunk_overlap)
        st.write(f"Number of chunks: {len(chunks)}")
        return chunks