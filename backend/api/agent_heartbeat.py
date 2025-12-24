from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.databases.db import get_db
from backend.models.core_models import AgentPC, AgentHeartbeat

router = APIRouter()

@router.post("/agent/heartbeat")
def agent_heartbeat(data: dict, db: Session = Depends(get_db)):
    pc_id = data.get("pc_id")
    status = data.get("status", "online")

    agent = db.query(AgentPC).filter(AgentPC.pc_id == pc_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not registered")
    
    agent.last_seen = datetime.utcnow()
    db.add(agent)
    
    heartbeat = AgentHeartbeat(
        pc_id=pc_id,
        status=status
    )
    
    db.add(heartbeat)
    db.commit()
    
    return {"message": "heartbeat received"}
