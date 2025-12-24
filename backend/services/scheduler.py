import time
import threading

from backend.services.log_processor import process_raw_logs

class LogProcessingScheduler:
    def __init__(self, interval_seconds: int = 10, batch_size: int = 100):
        self.interval_seconds = interval_seconds
        self.batch_size = batch_size
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        
    def start(self):
        if not self._thread.is_alive():
            self._thread.start()
            print("[SCHEDULER] Log processor started")
    
    def stop(self):
        self._stop_event.set()
        print("[SCHEDULER] Log processor stopped")
        
    def _run(self):
        while not self._stop_event.is_set():
            try:
                process_raw_logs(self.batch_size)
            except Exception as e:
                print(f"[SCHEDULER ERROR] {e}")
                
            time.sleep(self.interval_seconds)