# backend/models/alert_models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from backend.databases.db import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    classified_log_id = Column(
        Integer,
        ForeignKey("classified_logs.id"),
        nullable=False
    )

    pc_id = Column(String(100), index=True, nullable=False)

    severity = Column(String(20))  # high / critical
    message = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
