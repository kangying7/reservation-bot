import subprocess
import time
import random

from multiprocessing import Process, Queue, current_process, freeze_support

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


def test():
    NUMBER_OF_PROCESSES = 2
    TASKS1 = [(mul, (i, 7)) for i in range(10)]


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
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Get and print results
    print('Unordered results:')
    for i in range(len(TASKS1)):
        print('\t', done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')
    
    # # Stop/join all worker processes
    # for i in range(NUMBER_OF_PROCESSES):
    #     Process(target=worker, args=(task_queue, done_queue)).join()


if __name__ == '__main__':
    freeze_support()
    test()
