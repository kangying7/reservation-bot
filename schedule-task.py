import schedule
import time
from file_to_run import main as file_to_run_main

def job():
    file_to_run_main()

for timeslot in ["14:11", "14:12", "14:13"]:
    schedule.every().wednesday.at(timeslot).do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

