import socket
import subprocess
import platform
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.databases.db import get_db
from backend.models.core_models import AgentPC

router = APIRouter(prefix="/deployment", tags=["deployment"])

def get_local_subnet():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    parts = local_ip.split(".")
    return ".".join(parts[:3]) + ".", local_ip

def ping_ip(ip: str):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    subprocess.run(
        ["ping", param, "1", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def read_arp_table():
    result = subprocess.check_output("arp -a", shell=True).decode()
    devices = []

    for line in result.splitlines():
        if "-" in line and "." in line:
            parts = line.split()
            ip = parts[0]
            devices.append(ip)

    return list(set(devices))

def resolve_hostname(ip: str):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None


@router.get("/discover")
def discover_pcs(db: Session = Depends(get_db)):
    subnet, local_ip = get_local_subnet()

    # Ping sweep
    for i in range(1, 255):
        ip = f"{subnet}{i}"
        if ip != local_ip:
            ping_ip(ip)

    discovered_ips = read_arp_table()

    results = []

    for ip in discovered_ips:
        hostname = resolve_hostname(ip)

        agent = (
            db.query(AgentPC)
            .filter(AgentPC.ip_address == ip)
            .first()
        )

        results.append({
            "ip": ip,
            "hostname": hostname,
            "agent_installed": bool(agent),
            "last_seen": agent.last_seen if agent else None
        })

    return {
        "local_ip": local_ip,
        "count": len(results),
        "pcs": results
    }
