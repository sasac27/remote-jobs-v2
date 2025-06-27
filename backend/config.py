import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  
    SQLALCHEMY_TRACK_MODIFICATIONS = False               
    PREFERRED_URL_SCHEME = "https"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True if you're enforcing HTTPS
    REMEMBER_COOKIE_HTTPONLY = True
