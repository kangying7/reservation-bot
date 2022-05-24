import asyncio
from calendar import FRIDAY, MONDAY, THURSDAY, TUESDAY, WEDNESDAY
from lib.custom_logger import CustomLogger
from pathlib import Path
import datetime
from timeit import default_timer as timer

async def run(cmd, logger: CustomLogger):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    logger.add_to_log(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        logger.add_to_log(f'[stdout]\n{stdout.decode()}')
    if stderr:
        logger.add_to_log(f'[stderr]\n{stderr.decode()}')

async def single_session_run(end_time, days, log_dest, enable_booking: bool):
    session_logger = CustomLogger(log_dest, "session_details.log")
    start_time = datetime.datetime.now()

    coros = [run(f'python ./automate_reservation.py --time {end_time} --log "{log_dest}" --day {weekday} {"--booking" if enable_booking else ""}', session_logger) for weekday in days]
    # coros = [run(f'python ./automate_reservation.py --time {time} --log "{session_log_path}" --day {weekday} --booking', session_logger) for weekday in [FRIDAY]]

    await asyncio.gather(*coros)
    end_time = datetime.datetime.now()
    time_taken_to_complete = end_time - start_time
    session_logger.add_to_log(f"Session started at {start_time} and ended at {end_time}, taking {time_taken_to_complete}s to complete")

async def main():
    # Running single session

    time = "7:30"
    # Create output folder if it does not exist
    log_output_path = Path.cwd() / 'output'
    Path(log_output_path).mkdir(parents=True, exist_ok=True)

    # Create log folder with timestamp
    session_log_path = log_output_path / f'session_{datetime.datetime.now().strftime("%b_%d_%H%M_%S_%f")}'
    Path(session_log_path).mkdir()

    await single_session_run(time, [TUESDAY, WEDNESDAY, THURSDAY, FRIDAY], session_log_path, False)

if __name__ == "__main__":
    asyncio.run(main())