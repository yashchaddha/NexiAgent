from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from the root directory
load_dotenv("../.env")

# Database configuration - use existing POSTGRES_URI
DATABASE_URL = os.getenv("POSTGRES_URI")

if not DATABASE_URL:
    raise ValueError("POSTGRES_URI environment variable is required")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
