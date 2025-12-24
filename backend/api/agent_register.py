import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.databases.db import get_db
from backend.models.core_models import AgentPC

router = APIRouter()

@router.post("/agent/register")
def register_agent(data: dict, db: Session = Depends(get_db)):
    pc_id = str(uuid.uuid4())
    
    agent = AgentPC(
        pc_id = pc_id,
        hostname = data['hostname'],
        ip_address = data['ip_address'],
        os_type=data["os_type"],
        agent_version=data.get("agent_version", "unknown")
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return {"PC id": pc_id}
    