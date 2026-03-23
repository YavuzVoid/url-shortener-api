import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./url_shortener.db")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
