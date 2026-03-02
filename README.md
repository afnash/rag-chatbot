# University Admission Portal RAG Chatbot

This project is a production-ready AI-driven chatbot integrated into a University Admission Portal. It leverages Retrieval-Augmented Generation (RAG) and structured database integration to provide accurate, grounded responses.

## Architecture

The system follows a modular backend architecture using **FastAPI** and **PostgreSQL**. 
- **RAG Pipeline**: Built with LangChain, FAISS, and Gemini 1.5 Flash. Documents (PDF/CSV) are ingested, chunked, and stored as embeddings.
- **Database**: PostgreSQL handles persistent storage for application records and logs every user query for traceability.
- **Frontend**: A minimal vanilla HTML/JS interface with an embedded chat widget.

## RAG Pipeline

1. **Ingestion**: Documents in the `documents/` folder are processed. CSV rows are converted into structured text strings (e.g., "Program: Computer Science. Deadline: Dec 1").
2. **Chunking**: `RecursiveCharacterTextSplitter` ensures contexts fits within prompt limits while maintaining semantic meaning.
3. **Retrieval**: FAISS provides high-performance similarity search to find the top 3 most relevant context snippets.
4. **Grounding**: The LLM is strictly instructed to only use the provided context. Any out-of-scope question is met with a standard refusal.

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- PostgreSQL instance running

### 2. Environment Variables
Copy `.env.example` to `.env` and fill in:
- `GEMINI_API_KEY`: Your Google Gemini API key.
- `DATABASE_URL`: PostgreSQL connection string (`postgresql://user:pass@host:port/db`).

### 3. Installation
```bash
pip install -r requirements.txt
```

### 4. Data Ingestion
Place your `prospectus.pdf`, `admission_rules.pdf`, and `programs.csv` in the `documents/` folder, then run:
```bash
export PYTHONPATH=$PYTHONPATH:.
python backend/rag/ingestion.py
```

### 5. Running Locally
```bash
uvicorn backend.main:app --reload
```
Access the portal at `http://127.0.0.1:8000/`.

## API Endpoints
- `POST /api/chat/`: Grounded RAG chat + direct application status lookup.
- `GET /api/status/{app_id}`: Retrieve application status.
- `PUT /api/status/update-status`: Update application status via JSON body.
