import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///justice_ai.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ML Model settings
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/legal_bert_model')
    MAX_SEQUENCE_LENGTH = 512
    
    # API settings
    API_TITLE = 'JusticeAI API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'} 