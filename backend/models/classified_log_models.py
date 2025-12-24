from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.sql import func
from backend.databases.db import Base

class ClassifiedLog(Base):
    __tablename__ = "classified_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    raw_log_id = Column(Integer, ForeignKey('raw_logs.id'), nullable=False)
    
    pc_id = Column(String(100), index=True, nullable=False)

    source = Column(String(50))
    log_type = Column(String(50))

    cleaned_content = Column(Text)

    classification = Column(String(50), index=True)
    confidence = Column(Float)
    risk_level = Column(String(20))  # low / medium / high

    model_version = Column(String(20))

    classified_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )