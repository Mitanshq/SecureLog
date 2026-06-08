import win32evtlog
from datetime import datetime
import sqlite3
import shutil
import os

def collect_usb_setupapi_logs(max_lines=2000):
    logs = []
    log_path = r"C:\Windows\INF\setupapi.dev.log"

    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[-max_lines:]

        for line in lines:
            if "USBSTOR" in line or "DiskDrive" in line:
                logs.append({
                    "timestamp": None,
                    "source": "usb",
                    "type": "setupapi",
                    "content": line.strip()
                })

    except Exception:
        pass

    return logs


def collect_chrome_history(limit=250):
    logs = []
    try:
        user = os.getlogin()
        history_path = (
            f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\"
            "User Data\\Default\\History"
        )

        if not os.path.exists(history_path):
            return logs

        temp_copy = "chrome_history_tmp.db"
        shutil.copyfile(history_path, temp_copy)

        conn = sqlite3.connect(temp_copy)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT url, title
            FROM urls
            ORDER BY last_visit_time DESC
            LIMIT ?
        """, (limit,))

        for url, title in cursor.fetchall():
            logs.append({
                "timestamp": None,
                "source": "browser",
                "type": "chrome_history",
                "content": f"Visited URL: {url}"
            })

        conn.close()
        os.remove(temp_copy)

    except Exception:
        pass

    return logs

def collect_usb_events(max_events=300):
    logs = []
    server = "localhost"
    log_type = "System"

    try:
        handle = win32evtlog.OpenEventLog(server, log_type)
        flags = (
            win32evtlog.EVENTLOG_BACKWARDS_READ |
            win32evtlog.EVENTLOG_SEQUENTIAL_READ
        )

        events = win32evtlog.ReadEventLog(handle, flags, 0)
        if not events:
            return logs

        for event in events[:max_events]:
            event_id = event.EventID & 0xFFFF  # important masking

            if event_id in (2003, 2102):
                logs.append({
                    "timestamp": event.TimeGenerated.Format(),
                    "source": "usb",
                    "type": "device_event",
                    "content": f"USB event {event_id}: {event.StringInserts}"
                })

    except Exception:
        pass

    return logs



def collect_windows_logs(max_events=500):
    logs = []
    server = 'localhost'
    log_types = ['System', 'Aplication']
    
    for log_type in log_types:
        handle = win32evtlog.OpenEventLog(server, log_type)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        
        events = win32evtlog.ReadEventLog(handle, flags, 0)
        if not events:
            continue
        
        for event in events[:max_events]:
            logs.append({
                "timestamp": event.TimeGenerated.Format(),
                "source": log_type,
                "type": "windows_event",
                "content": str(event.StringInserts)
            })
            
    return logs