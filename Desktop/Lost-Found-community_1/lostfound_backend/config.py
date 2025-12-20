import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    # SHARED SECRET KEYS: Everyone must use these same strings
    SECRET_KEY = "lostfound-team-shared-key-2025"
    JWT_SECRET_KEY = "lostfound-team-shared-key-2025"
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'data.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Uploads
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}