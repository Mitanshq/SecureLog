from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from backend.databases.db import Base


class LabeledLog(Base):
    __tablename__ = "labeled_logs"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String(50), nullable=False)
    log_type = Column(String(50), nullable=False)

    content = Column(Text, nullable=False)

    label = Column(
        String(20),
        nullable=False  # genuine / malicious
    )

    label_source = Column(
        String(50),
        nullable=False  # public_dataset / rule / human
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
