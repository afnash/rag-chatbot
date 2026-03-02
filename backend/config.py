import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()
