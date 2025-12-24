# Stores all configuration
# Avoids hardcoding values
# Makes scaling + deployment easy
# Is imported everywhere else

# backend/config/config.py

import os

# ======================
# ENVIRONMENT
# ======================
ENV = os.getenv("ENV", "development")

# ======================
# SERVER SETTINGS
# ======================
API_HOST = "0.0.0.0"
API_PORT = 8000

# ======================
# SECURITY
# ======================
SECRET_KEY = os.getenv("SECRET_KEY", "securelog-secret")
LOG_ENCRYPTION_KEY = os.getenv("LOG_ENCRYPTION_KEY", "log-encryption-key")

# ======================
# DATABASE CONFIG
# ======================
POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql://postgres:securelog%40123@localhost:5432/securelog"
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)

# ======================
# QUEUE CONFIG (future)
# ======================
RAW_LOG_TOPIC = "raw_logs"
PROCESSED_LOG_TOPIC = "processed_logs"
ALERT_TOPIC = "alerts"

# ======================
# AGENT SETTINGS
# ======================
LOG_BATCH_INTERVAL_SECONDS = 120
MAX_LOG_BATCH_SIZE = 5000

# ======================
# AI SETTINGS
# ======================
CONFIDENCE_THRESHOLD = 0.97
MODEL_VERSION = "v1.0"
