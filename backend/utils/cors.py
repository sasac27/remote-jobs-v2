from flask_cors import cross_origin
import os

def dynamic_cors():
    origin = os.getenv("CORS_ORIGIN", "http://localhost:4200")
    return cross_origin(origins=[origin], supports_credentials=True)
