# agent/config.py

SERVER_URL = "http://127.0.0.1:8000"
LOG_UPLOAD_ENDPOINT = "/api/agent/logs"
REGISTER_ENDPOINT = "/api/agent/register"
HEARTBEAT_ENDPOINT = "/api/agent/heartbeat"

LOG_BATCH_INTERVAL = 10  # seconds
HEARTBEAT_INTERVAL = 5

AGENT_VERSION = "1.0.0"

PC_ID_FILE = "pc_id.txt"
