from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database.db import get_db
from backend.database.models import Application

router = APIRouter()

class StatusUpdate(BaseModel):
    application_id: str
    applicant_name: str = None
    program: str = None
    new_status: str = None

@router.get("/")
async def get_all_applications(db: Session = Depends(get_db)):
    return db.query(Application).all()

@router.get("/{app_id}")
async def get_application_status(app_id: str, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return {
        "id": application.id,
        "applicant_name": application.applicant_name,
        "status": application.status,
        "program": application.program
    }

@router.put("/update-status")
async def update_status(update_data: StatusUpdate, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == update_data.application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if update_data.applicant_name:
        application.applicant_name = update_data.applicant_name
    if update_data.program:
        application.program = update_data.program
    if update_data.new_status:
        application.status = update_data.new_status
        
    db.commit()
    return {"message": "Application updated successfully", "application": {
        "id": application.id,
        "applicant_name": application.applicant_name,
        "status": application.status,
        "program": application.program
    }}

@router.get("/")
async def get_backend_status():
    return {"status": "Backend is running smoothly"}
