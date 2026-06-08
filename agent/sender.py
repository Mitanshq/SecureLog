import requests
from agent.config import SERVER_URL, LOG_UPLOAD_ENDPOINT

def send_logs(pc_id: str, logs: list):
    if not logs:
        return

    payload = {
        "pc_id": pc_id,
        "logs": logs
    }

    try:
        requests.post(
            SERVER_URL + LOG_UPLOAD_ENDPOINT,
            json=payload,
            timeout=10
        )
    except Exception:
        pass