import datetime
from pathlib import Path
from pickle import NONE
import subprocess
import time
import random
from calendar import FRIDAY, THURSDAY, TUESDAY, WEDNESDAY
from multiprocessing import Process, Queue, current_process, freeze_support, cpu_count
from lib.custom_logger import CustomLogger

#
# Function run by worker processes
#

def worker(input_queue: Queue, output_queue: Queue):
    for func, args in iter(input_queue.get, 'STOP'):
        result = calculate(func, args)
        output_queue.put(result)

#
# Function used to calculate result
#


def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % \
        (current_process().name, func.__name__, args, result)

#
# Functions referenced by tasks
#


def mul(a, b):
    time.sleep(0.5*random.random())
    return a * b


def plus(a, b):
    time.sleep(0.5*random.random())
    return a + b

#
#
#

def work(cmd):
    return subprocess.run(cmd, shell=True)

def create_session(end_time, days, log_dest, enable_booking: bool, task_queue, done_queue):
    session_logger = CustomLogger(log_dest, "session_details.log")
    start_time = datetime.datetime.now()

    task_queue.put([(subprocess.run, f'python ./automate_reservation.py --time {end_time} --log "{log_dest}" --day {weekday} {"--booking" if enable_booking else ""}') for weekday in days])

    end_time = datetime.datetime.now()
    time_taken_to_complete = end_time - start_time
    session_logger.add_to_log(f"Session started at {start_time} and ended at {end_time}, taking {time_taken_to_complete}s to complete")

def worker_3(input_queue: Queue, output_queue: Queue):
    for func, args in iter(input_queue.get, 'STOP'):
        result = execute_command(func, args) 
        output_queue.put(result)

def execute_command(func, args):    
    print("Function to run is", func)
    print("Args to run is", *args)
    return func(*args)


def worker_2(input_queue: Queue, output_queue: Queue):
    for cmd in iter(input_queue.get, 'STOP'):
        # result = calculate(func, args)
        print("Command to run is", cmd)
        result = subprocess.run(cmd, shell=True, capture_output=True)
        output_queue.put(result)

def test():
    # NUMBER_OF_PROCESSES = cpu_count()
    NUMBER_OF_PROCESSES = 2
    time = "7:30"
    # Create output folder if it does not exist
    log_output_path = Path.cwd() / 'output'
    Path(log_output_path).mkdir(parents=True, exist_ok=True)

    # Create log folder with timestamp
    session_log_path = log_output_path / f'session_{datetime.datetime.now().strftime("%b_%d_%H%M_%S_%f")}'
    Path(session_log_path).mkdir()
    session_logger = CustomLogger(session_log_path, "session_details.log")


    # TASKS1 = [f'python ./automate_reservation.py --time {time} --log "{session_log_path}" --day {weekday} --booking' for weekday in [TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]]
    # print("Task is", TASKS1)

    TASKS1 = [(subprocess.run, f'python ./automate_reservation.py --time {time} --log "{session_log_path}" --day {weekday} --booking', 'shell=True') for weekday in [TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]]
    # print("Task is", TASKS1)
    # manager = Manager()
    # results_dict = manager.dict()
    
    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS1:
        task_queue.put(task)

    # Start worker processes 
    # Distribute tasks to worker based on queue
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker_3, args=(task_queue, done_queue)).start()

    # # Get and print results
    # print('Unordered results:')
    # for i in range(len(TASKS1)):
    #     print('\t', done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')
    
    # # Stop/join all worker processes
    # for i in range(NUMBER_OF_PROCESSES):
    #     Process(target=worker, args=(task_queue, done_queue)).join()


if __name__ == '__main__':
    freeze_support()
    test()
