from flask_cors import cross_origin
import os

def dynamic_cors():
    # Use your Render frontend domain as default now
    origin = os.getenv("CORS_ORIGIN", "https://remote-jobs-v2-1.onrender.com")
    return cross_origin(origins=[origin], supports_credentials=True)
