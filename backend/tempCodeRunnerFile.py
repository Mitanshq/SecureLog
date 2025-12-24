from fastapi import FastAPI
from backend.databases.db import engine
from backend.models.core_models import Base
from backend.models.log_models import RawLog
from backend.api.agent_register import router as agent_router
from backend.api.agent_heartbeat import router as heartbeat_router


app = FastAPI(title='SecureLog')
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
app.include_router(agent_router, prefix="/api")
app.include_router(heartbeat_router, prefix="/api")


@app.get('/')
def health_check():
    return {"status": "SecureLog server running"}