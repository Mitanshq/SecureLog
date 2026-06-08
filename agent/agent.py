# agent/agent.py

import time
import threading

from .register import register_agent
from .heartbeat import heartbeat_loop
from .collector import collect_windows_logs, collect_usb_events, collect_chrome_history, collect_usb_setupapi_logs
from .sender import send_logs
from .config import HEARTBEAT_INTERVAL, LOG_BATCH_INTERVAL

def main():
    pc_id = register_agent()

    hb_thread = threading.Thread(
        target=heartbeat_loop,
        args=(pc_id, HEARTBEAT_INTERVAL),
        daemon=True
    )
    hb_thread.start()


    while True:
        logs = []
        logs.extend(collect_windows_logs())
        logs.extend(collect_usb_events())          # keep (may work on some PCs)
        logs.extend(collect_usb_setupapi_logs())   # reliable fallback
        logs.extend(collect_chrome_history())

        send_logs(pc_id, logs)
        time.sleep(LOG_BATCH_INTERVAL)


if __name__ == "__main__":
    main()
