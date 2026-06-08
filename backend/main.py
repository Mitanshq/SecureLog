from fastapi import FastAPI
import os
from backend.databases.db import engine
from backend.models.core_models import Base
from backend.models.log_models import RawLog
from backend.models.classified_log_models import ClassifiedLog
from backend.models.user import User
from backend.api.agent_register import router as agent_router
from backend.api.auth import router as auth_router
from backend.api.agent_heartbeat import router as heartbeat_router
from backend.api.log_ingest import router as log_router
from backend.services.scheduler import LogProcessingScheduler
from backend.models.alert_models import Alert
from backend.api.dashboard import router as dashboard_router
from fastapi.staticfiles import StaticFiles
from backend.api.deployment import router as deployment_router


app = FastAPI(title='SecureLog')
scheduler = LogProcessingScheduler(interval_seconds=10, batch_size=100)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.stop()
    
app.include_router(dashboard_router, prefix="/api")
    
app.include_router(agent_router, prefix="/api")
app.include_router(heartbeat_router, prefix="/api")
app.include_router(log_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(deployment_router, prefix="/api")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount(
    "/",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True),
    name="frontend"
)