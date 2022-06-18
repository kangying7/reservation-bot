import asyncio
from calendar import FRIDAY, MONDAY, SUNDAY, THURSDAY, TUESDAY, WEDNESDAY, day_name, day_abbr
from configparser import ConfigParser
import shutil
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


async def main():
    # Create output folder if it does not exist
    log_output_path = Path.cwd() / 'output'
    Path(log_output_path).mkdir(parents=True, exist_ok=True)

    # Create log folder with timestamp
    session_log_path = log_output_path / f'session_{datetime.datetime.now().strftime("%b_%d_%H%M_%S_%f")}'
    Path(session_log_path).mkdir()

    # Copy over source config file to current session directory
    config_source_file = Path.cwd() / "etc" / "config.txt"
    config_session_file = shutil.copy(config_source_file, session_log_path)

    config = ConfigParser()
    config.read(config_session_file)
    single_run = config['single_run']
    reservation_start_time_range = single_run.get('start_time_range')
    reservation_end_time_range = single_run.get('end_time_range')
    days_to_book = single_run.get('days_to_book')
    session = single_run.get('session')
    booking = single_run.getboolean('booking')

    # Guard for days to book
    days_to_book_list = []
    try:
        for day in days_to_book.split(","):
            parsed_day = int(day.strip())
            days_to_book_list.append(parsed_day)
    except Exception as e:
        print(f"Error in config file: days_to_book parameter should be between 0-6 (Monday to Sunday), separated by comma. Error is: {e}")
        return

    # Create session_details file for logging purposes
    session_logger = CustomLogger(session_log_path, "session_details.log")
    start_time = datetime.datetime.now()

    # coros = [run(f'python ./automate_reservation.py --time {time} --log "{session_log_path}" --day {weekday} --booking', session_logger) for weekday in [TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]]
    coros = [run(f'python ./automate_reservation.py --start-time "{reservation_start_time_range}" --end-time "{reservation_end_time_range}" \
        --log "{session_log_path}" --day {weekday} --session {session} {"--booking" if booking else ""}',
                 session_logger) for weekday in days_to_book_list]

    await asyncio.gather(*coros)
    end_time = datetime.datetime.now()
    time_taken_to_complete = end_time - start_time
    session_logger.add_to_log(f"Session started at {start_time} and ended at {end_time}, taking {time_taken_to_complete}s to complete")

if __name__ == "__main__":
    asyncio.run(main())
