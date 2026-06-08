# agent/heartbeat.py

import time
import requests

from agent.config import SERVER_URL, HEARTBEAT_ENDPOINT


def send_heartbeat(pc_id: str):
    payload = {
        "pc_id": pc_id,
        "status": "online"
    }

    try:
        requests.post(
            SERVER_URL + HEARTBEAT_ENDPOINT,
            json=payload,
            timeout=5
        )
    except Exception:
        pass


def heartbeat_loop(pc_id: str, interval: int):
    while True:
        send_heartbeat(pc_id)
        time.sleep(interval)
