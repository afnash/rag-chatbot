import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, CSVLoader, BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from backend.config import settings

def ingest_documents(directory_path: str = "documents", frontend_path: str = "frontend"):
    """
    Ingests PDF, CSV, and HTML documents, chunks them, generates embeddings, and saves to FAISS.
    """
    print(f"Starting ingestion from {directory_path} and {frontend_path}...")
    
    documents = []
    
    if os.path.exists(directory_path):
        pdf_loader = DirectoryLoader(directory_path, glob="./*.pdf", loader_cls=PyPDFLoader)
        documents.extend(pdf_loader.load())
        
        csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
        for csv_file in csv_files:
            df = pd.read_csv(os.path.join(directory_path, csv_file))
            for _, row in df.iterrows():
                row_text = ". ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                documents.append(Document(page_content=row_text, metadata={"source": csv_file}))

    if os.path.exists(frontend_path):
        html_files = [f for f in os.listdir(frontend_path) if f.endswith('.html') and f != 'admin.html']
        for html_file in html_files:
            loader = BSHTMLLoader(os.path.join(frontend_path, html_file))
            documents.extend(loader.load())
            
    print(f"Loaded {len(documents)} total documents/rows.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks.")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=settings.GEMINI_API_KEY)
    
    vector_db = FAISS.from_documents(texts, embeddings)
    
    if not os.path.exists(settings.VECTOR_DB_PATH):
        os.makedirs(settings.VECTOR_DB_PATH)
    
    vector_db.save_local(settings.VECTOR_DB_PATH)
    print(f"Vector database saved to {settings.VECTOR_DB_PATH}")
    
    return True

if __name__ == "__main__":
    ingest_documents()
