import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    UPLOAD_EXTENSIONS = ['.mp4', '.avi', '.mov']
