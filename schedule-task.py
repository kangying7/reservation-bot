from asyncio import subprocess
from calendar import FRIDAY, MONDAY, THURSDAY, TUESDAY, WEDNESDAY
import schedule
import time
from file_to_run import main as file_to_run_main
from automate_reservation import main as automate_reservation_main
from automate_reservation import driver as automate_reservation_driver
import asyncio
# async def job():
#     # file_to_run_main()
#     # automate_reservation_main("07:30", False)
#     coros = [automate_reservation_driver("07:30", weekday, False) for weekday in [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]]
#     await asyncio.gather(*coros)

# for timeslot in ["18:44"]:
#     schedule.every().wednesday.at(timeslot).do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)


# asyncio.run(job()) 