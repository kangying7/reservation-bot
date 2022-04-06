import schedule
import time
from file_to_run import main as file_to_run_main
from automate_reservation import main as automate_reservation_main

def job():
    # file_to_run_main()
    automate_reservation_main("07:30", False)

for timeslot in ["18:44"]:
    schedule.every().wednesday.at(timeslot).do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

