import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    PORT = int(os.getenv("PORT", 5000))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///employees.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
