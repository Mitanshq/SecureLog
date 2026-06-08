import os
import socket
import requests

from agent.config import SERVER_URL, REGISTER_ENDPOINT, PC_ID_FILE, AGENT_VERSION

def get_pc_metadata():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_type = "Windows"

    return {
        "hostname": hostname,
        "ip_address": ip_address,
        "os_type": os_type,
        "agent_version": AGENT_VERSION
    }
    
def register_agent():
    if os.path.exists(PC_ID_FILE):
        with open(PC_ID_FILE, 'r') as f:
            return f.read().strip()
        
    payload = get_pc_metadata()
    response = requests.post(
        SERVER_URL + REGISTER_ENDPOINT,
        json=payload,
        timeout=10
    )
    response.raise_for_status()
    
    data = response.json()
    pc_id = data["pc_id"]
    
    with open(PC_ID_FILE, "w") as f:
        f.write(pc_id)
        
    return pc_id