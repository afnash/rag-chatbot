from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from backend.routes import chat, status
from backend.database.db import engine
from backend.database.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG Chatbot API")

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(status.router, prefix="/api/status", tags=["status"])

# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join("frontend", "index.html"))

@app.get("/{page}.html")
async def read_html(page: str):
    path = os.path.join("frontend", f"{page}.html")
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "Page not found"}
    
port = int(os.environ.get("PORT", 8000))