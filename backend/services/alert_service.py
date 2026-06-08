# backend/services/alert_service.py

from sqlalchemy.orm import Session
from backend.models.alert_models import Alert
from backend.models.classified_log_models import ClassifiedLog


def generate_alert_if_needed(
    db: Session,
    classified_log: ClassifiedLog
):
    if classified_log.risk_level != "high":
        return

    alert = Alert(
        classified_log_id=classified_log.id,
        pc_id=classified_log.pc_id,
        severity="high",
        message=(
            f"Malicious activity detected: "
            f"{classified_log.classification}"
        )
    )

    db.add(alert)
