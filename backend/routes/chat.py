from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db import get_db
import re
from backend.database.models import UserQuery, Application
from backend.rag.retriever import retrieve_context

router = APIRouter()

@router.get("/logs")
async def get_chat_logs(db: Session = Depends(get_db)):
    return db.query(UserQuery).order_by(UserQuery.timestamp.desc()).limit(50).all()

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    return db.query(UserQuery).filter(UserQuery.session_id == session_id).order_by(UserQuery.timestamp.asc()).all()

@router.post("/")
async def chat(message: str, session_id: str = "default", db: Session = Depends(get_db)):
    try:
        app_id_match = re.search(r'\bA\d{4}\b', message.upper())
        if app_id_match:
            app_id = app_id_match.group()
            application = db.query(Application).filter(Application.id == app_id).first()
            if application:
                response_text = f"Yes, I found it! The status for application {app_id} (belonging to {application.applicant_name}) is currently '{application.status}'. This is for the {application.program} program."
            else:
                response_text = f"I'm sorry, I couldn't find any record for an application with the ID {app_id}. Could you please double-check the ID?"
            
            new_query = UserQuery(session_id=session_id, query=message, response=response_text)
            db.add(new_query)
            db.commit()
            return {"response": response_text}

        history_records = db.query(UserQuery).filter(UserQuery.session_id == session_id)\
            .order_by(UserQuery.timestamp.desc()).limit(5).all()
        
        history_text = ""
        for rec in reversed(history_records):
            history_text += f"User: {rec.query}\nAssistant: {rec.response}\n"

        response_text, sources = retrieve_context(message, chat_history=history_text)
        
        new_query = UserQuery(session_id=session_id, query=message, response=response_text)
        db.add(new_query)
        db.commit()

        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
