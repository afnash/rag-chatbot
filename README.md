# 🎓 University Admission Assistant (RAG Chatbot)

Welcome to the **University Admission Assistant**! This is an AI-powered portal designed to help prospective students learn about university programs, tuition fees, and check their application status using a modern RAG (Retrieval-Augmented Generation) pipeline.

---

## 🛠️ How it Works (For Beginners)

This project uses a technique called **RAG (Retrieval-Augmented Generation)**. 

Imagine you have a very smart assistant (the Large Language Model, or LLM) who knows a lot about the world but doesn't know anything about *your* specific university. 
1.  **Ingestion**: We take your university documents (PDFs, CSVs) and "teach" them to the assistant by storing them in a searchable database.
2.  **Retrieval**: When a student asks a question like "What is the fee for BTech AI?", the system searches your documents for the answer.
3.  **Generation**: The system gives the relevant text to the LLM, which then writes a polite, natural-sounding response back to the student.

---

## 🚀 Quick Start Guide

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
- **Python 3.10 or higher** installed on your system.
- A **Google Gemini API Key** (it's free!). Get it at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Setup the Environment
First, clone the repository and navigate into the folder:

```bash
# Create a virtual environment to keep dependencies organized
python3 -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the template file to create your own configuration:
```bash
cp .env.example .env
```
Open the `.env` file and paste your **GEMINI_API_KEY**. By default, the project uses **SQLite** (a simple file-based database), so you don't need to install PostgreSQL to get started!

### 5. Ingest Your Data
Before the chatbot can answer questions, it needs to "read" your documents. Place your PDF or CSV files in the `documents/` folder.
```bash
# This script processes your documents and creates the vector database
export PYTHONPATH=$PYTHONPATH:.
python3 backend/rag/ingestion.py
```

### 6. Launch the App!
Start the backend server:
```bash
uvicorn backend.main:app --reload
```
Now, open your browser and go to: **[http://localhost:8000](http://localhost:8000)**

---

## 📂 Project Structure

- `backend/`: The logic of the app (FastAPI routes, RAG pipeline, Database models).
- `frontend/`: Static HTML/CSS files for the website and chat widget.
- `documents/`: Your source data (PDFs/CSVs) that the AI reads.
- `vector_storage/`: Where the AI's "brain" (processed documents) is saved.

---

## 💡 Changing Databases (Intermediate)
If you want to move from **SQLite** (local file) to **PostgreSQL** (production):
1.  Install PostgreSQL on your machine.
2.  Update the `DATABASE_URL` in your `.env` file.
3.  The app will automatically create the required tables on the next startup!

---

## 📝 API Endpoints
- `POST /api/chat/`: Send a message to the AI Assistant.
- `GET /api/status/{app_id}`: Check the status of a specific application (e.g., A1001).
