# backend/api/log_ingest.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.databases.db import get_db
from backend.models.core_models import AgentPC
from backend.models.log_models import RawLog


router = APIRouter()

@router.post("/agent/logs")
def ingest_logs(data: dict, db: Session = Depends(get_db)):
    pc_id = data.get("pc_id")
    logs = data.get("logs", [])

    if not pc_id or not logs:
        raise HTTPException(status_code=400, detail="Invalid payload")

    agent = db.query(AgentPC).filter(AgentPC.pc_id == pc_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not registered")

    raw_log_objects = []

    for log in logs:
        ts = log.get("timestamp")
        parsed_ts = None

        if ts:
            try:
                parsed_ts = datetime.fromisoformat(ts)
            except ValueError:
                parsed_ts = None
                
        raw_log = RawLog(
            pc_id=pc_id,
            source=log.get("source"),
            log_type=log.get("type"),
            content=log.get("content"),
            timestamp=parsed_ts
        )
        raw_log_objects.append(raw_log)

    db.bulk_save_objects(raw_log_objects)
    db.commit()

    return {
        "message": "logs received",
        "count": len(raw_log_objects)
    }
