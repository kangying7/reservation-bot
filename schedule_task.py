import subprocess
import threading
from datetime import datetime
import time
import sched
from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.first_run = True
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if self.first_run:
            self._timer = Timer(0.5, self._run)
            self._timer.start()
            self.first_run = False

        elif not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def run_all_schedule():
    subprocess.run(f"python async_subprocess.py", shell=True)


def repeat_task_for_duration(run_time: int, interval: int):
    rt = RepeatedTimer(interval, run_all_schedule)
    try:
        time.sleep(run_time)
    finally:
        rt.stop()


if __name__ == "__main__":
    target_time: str = '2022-05-12 21:59:57'
    # target_time: str = '2022-05-12 21:47:05'

    run_time: int = 10
    interval: int = 4

    s = sched.scheduler(time.time, time.sleep)
    abs_target_time = datetime.strptime(target_time, '%Y-%m-%d %H:%M:%S').timestamp()

    s.enterabs(abs_target_time, 1, repeat_task_for_duration, argument=[run_time, interval])
    s.run()
