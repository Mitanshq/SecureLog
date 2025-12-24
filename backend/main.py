from fastapi import FastAPI
from backend.databases.db import engine
from backend.models.core_models import Base
from backend.models.log_models import RawLog
from backend.models.classified_log_models import ClassifiedLog
from backend.api.agent_register import router as agent_router
from backend.api.agent_heartbeat import router as heartbeat_router
from backend.api.log_ingest import router as log_router
from backend.services.scheduler import LogProcessingScheduler

app = FastAPI(title='SecureLog')
scheduler = LogProcessingScheduler(interval_seconds=10, batch_size=100)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.stop()
    
app.include_router(agent_router, prefix="/api")
app.include_router(heartbeat_router, prefix="/api")
app.include_router(log_router, prefix="/api")


@app.get('/')
def health_check():
    return {"status": "SecureLog server running"}