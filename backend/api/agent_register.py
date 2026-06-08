import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from backend.databases.db import get_db
from backend.models.core_models import AgentPC

router = APIRouter()

@router.post("/agent/register")
def register_agent(
    data: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    hostname = data.get("hostname")
    user_id = data.get("user_id") 

    if not hostname or not user_id:
        raise HTTPException(status_code=400, detail="hostname and user_id required")

    ip_address = request.client.host  # real IP

    # Check if agent already exists (same user + hostname)
    existing = (
        db.query(AgentPC)
        .filter(
            AgentPC.hostname == hostname,
            AgentPC.user_id == user_id  
        )
        .first()
    )

    if existing:
        existing.last_seen = datetime.now(datetime.timezone.utc)
        existing.ip_address = ip_address
        db.commit()

        return {"pc_id": existing.pc_id}

    pc_id = str(uuid.uuid4())

    agent = AgentPC(
        pc_id=pc_id,
        hostname=hostname,
        ip_address=ip_address,
        os_type=data.get("os_type", "unknown"),
        agent_version=data.get("agent_version", "unknown"),
        last_seen=datetime.now(datetime.timezone.utc),
        user_id=user_id   # ✅ LINK AGENT TO USER
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {"pc_id": pc_id}