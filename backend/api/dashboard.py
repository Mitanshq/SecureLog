# backend/api/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

from backend.databases.db import get_db
from backend.models.core_models import AgentPC
from backend.models.log_models import RawLog
from backend.models.classified_log_models import ClassifiedLog
from backend.models.alert_models import Alert

router = APIRouter()


# ===============================
# SUMMARY
# ===============================
@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

    total_logs = db.query(RawLog).count()
    total_classified = db.query(ClassifiedLog).count()
    total_alerts = db.query(Alert).count()

    active_agents = (
        db.query(AgentPC)
        .filter(AgentPC.last_seen >= five_minutes_ago)
        .count()
    )

    return {
        "total_logs": total_logs,
        "classified_logs": total_classified,
        "alerts": total_alerts,
        "active_agents": active_agents
    }


# ===============================
# ACTIVE PCS
# ===============================
@router.get("/dashboard/active-pcs")
def active_pcs(db: Session = Depends(get_db)):
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

    pcs = (
        db.query(AgentPC)
        .filter(AgentPC.last_seen >= five_minutes_ago)
        .all()
    )

    return [
        {
            "pc_id": pc.pc_id,
            "hostname": pc.hostname,
            "last_seen": pc.last_seen
        }
        for pc in pcs
    ]


# ===============================
# REGISTERED PCS
# ===============================
@router.get("/dashboard/registered-pcs")
def registered_pcs(db: Session = Depends(get_db)):
    five_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=5)

    pcs = db.query(AgentPC).order_by(AgentPC.last_seen.desc()).all()

    return [
        {
            "hostname": pc.hostname,
            "ip": pc.ip_address or "-",
            "installed": True,
            "active": pc.last_seen is not None and pc.last_seen >= five_minutes_ago,
            "last_seen": pc.last_seen.isoformat() if pc.last_seen else None
        }
        for pc in pcs
    ]


# ===============================
# ALERTS
# ===============================
@router.get("/dashboard/alerts")
def recent_alerts(limit: int = 20, db: Session = Depends(get_db)):
    alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "pc_id": a.pc_id,
            "severity": a.severity,
            "message": a.message,
            "time": a.created_at
        }
        for a in alerts
    ]


# ===============================
# LOGS BY SOURCE
# ===============================
@router.get("/dashboard/logs-by-source")
def logs_by_source(db: Session = Depends(get_db)):
    rows = (
        db.query(RawLog.source, func.count(RawLog.id))
        .group_by(RawLog.source)
        .all()
    )

    return {source: count for source, count in rows}


# ===============================
# LOGS BY RISK
# ===============================
@router.get("/dashboard/logs-by-risk")
def logs_by_risk(db: Session = Depends(get_db)):
    rows = (
        db.query(ClassifiedLog.risk_level, func.count(ClassifiedLog.id))
        .group_by(ClassifiedLog.risk_level)
        .all()
    )

    return {risk: count for risk, count in rows}


# ===============================
# PAGINATED LOGS
# ===============================
@router.get("/dashboard/logs")
def get_logs(
    page: int = 1,
    page_size: int = 20,
    source: str | None = None,
    db: Session = Depends(get_db)
):
    if page < 1:
        page = 1

    MAX_VISIBLE_LOGS = 2000

    base_query = db.query(RawLog, ClassifiedLog.risk_level).join(
        ClassifiedLog, RawLog.id == ClassifiedLog.raw_log_id
    )

    if source:
        base_query = base_query.filter(RawLog.source == source)

    subquery = (
        base_query
        .order_by(RawLog.received_at.desc())
        .limit(MAX_VISIBLE_LOGS)
        .subquery()
    )

    visible_query = db.query(subquery)

    total = visible_query.count()
    offset = (page - 1) * page_size

    results = (
        visible_query
        .order_by(subquery.c.received_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "logs": [
            {
                "source": result.source,
                "type": result.log_type,
                "content": result.content,
                "time": result.received_at,
                "category": result.risk_level
            }
            for result in results
        ]
    }