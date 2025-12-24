# backend/models/log_models.py

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from backend.databases.db import Base

class RawLog(Base):
    __tablename__ = "raw_logs"

    id = Column(Integer, primary_key=True, index=True)
    pc_id = Column(String(100), nullable=False)
    source = Column(String(50))
    log_type = Column(String(50))
    content = Column(Text)

    timestamp = Column(DateTime)
    received_at = Column(DateTime(timezone=True), server_default=func.now())

    processed = Column(Boolean, default=False, index=True)
