import subprocess
import threading
import datetime
from time import sleep
from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def run_all_schedule():
    subprocess.run(f"python async_subprocess.py")

def main():
    run_time: int = 30
    rt = RepeatedTimer(1, run_all_schedule)
    try:
        sleep(run_time) 
    finally:
        rt.stop()

if __name__ == "__main__":
    main()
