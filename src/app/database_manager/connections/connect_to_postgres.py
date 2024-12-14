# app/database_manager/connections.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from database_manager.models.models import Base
from settings.settings import settings


db_user = settings.DB_USER
db_passwd = settings.DB_PASSWORD
# Database URL (replace with your actual database URL)
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_passwd}@localhost/icustom"

# Create a new SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency to get the database session.
    This function is used in the FastAPI route handler to inject the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

