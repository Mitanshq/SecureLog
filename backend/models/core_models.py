from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.databases.db import Base

# ==========================
# ADMIN USER TABLE
# ==========================

# class AdminUser(Base):
#     __tablename__ = "admin_users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     Username = Column(String(50), unique=True, nullable=False)
#     password_hash = Column(String(255), nullable=False)
#     role = Column(String(20), default='admin')
#     is_active = Column(Boolean, default=True)
#     user_id = Column(Integer)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
    
# # ==========================
# AGENT PC TABLE
# ==========================

class AgentPC(Base):
    __tablename__ = "agent_pcs"
    
    id = Column(Integer, primary_key=True, index=True)
    pc_id = Column(String(100), unique=True, nullable=False)
    hostname = Column(String(100), nullable=False)
    ip_address = Column(String(50), nullable=False)
    os_type = Column(String(50), nullable=False)
    
    agent_version = Column(String(20))
    is_active = Column(Boolean, default=True)
    
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True))
    
# ==========================
# AGENT HEARTBEAT TABLE
# ==========================

class AgentHeartbeat(Base):
    __tablename__ = "agent_heartbeats"

    id = Column(Integer, primary_key=True, index=True)
    pc_id = Column(String(100), ForeignKey("agent_pcs.pc_id"))
    status = Column(String(20))  # online / offline
    timestamp = Column(DateTime(timezone=True), server_default=func.now())