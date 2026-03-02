from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.database.db import Base

from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from backend.database.db import Base

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(String, primary_key=True, index=True) # e.g., A1001
    applicant_name = Column(String)
    status = Column(String) # e.g., Pending, Approved, Rejected
    program = Column(String)

class UserQuery(Base):
    __tablename__ = "user_queries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    query = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
