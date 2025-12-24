# Creates safe, reusable database connections
# Prevents connection leaks
# Ensures high traffic does NOT crash the server
# Is used by every backend service

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config.config import POSTGRES_URL

# Engine

engine = create_engine(
    POSTGRES_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)

# Session Factory

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

# Base Model
Base = declarative_base()

# DB Dpendency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()