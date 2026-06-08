# backend/ai/ingest_public_data.py

from sqlalchemy.orm import Session
from backend.databases.db import SessionLocal
from backend.models.labeled_log import LabeledLog

DATASET_FILE = "backend/ai/datasets/powershell_attacks.txt"

def ingest():
    db: Session = SessionLocal()

    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        for line in f:
            content = line.strip()
            if not content:
                continue

            log = LabeledLog(
                source="application",
                log_type="process",
                content=content,
                label="malicious",
                label_source="public_dataset"
            )
            db.add(log)

    db.commit()
    db.close()

if __name__ == "__main__":
    ingest()
