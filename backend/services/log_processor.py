from sqlalchemy.orm import Session

from backend.databases.db import SessionLocal
from backend.models.log_models import RawLog
from backend.models.classified_log_models import ClassifiedLog
from backend.services.ai_inference import classify_log

def normalize_text(text: str):
    if not text:
        return ""
    return text.lower().strip()

def process_raw_logs(batch_size: int = 100):
    db : Session = SessionLocal()
    try:
        raw_logs = (
            db.query(RawLog)
            .filter(RawLog.processed == False)
            .order_by(RawLog.received_at.asc())
            .limit(batch_size)
            .all()
        )
        
        if not raw_logs:
            return
        
        for raw in raw_logs:
            cleaned_text = normalize_text(raw.content)
            
            ai_result = classify_log(cleaned_text)
            
            classified = ClassifiedLog(
                raw_log_id=raw.id,
                pc_id=raw.pc_id,
                source=raw.source,
                log_type=raw.log_type,
                cleaned_content=cleaned_text,
                classification=ai_result["classification"],
                confidence=ai_result["confidence"],
                risk_level=ai_result["risk_level"],
                model_version=ai_result["model_version"]
            )
            
            db.add(classified)
            raw.processed = True
        db.commit()
    
    finally:
        db.close()   