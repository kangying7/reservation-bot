import multiprocessing
import subprocess
import time
import random
import sys
from datetime import datetime

#
# Functions used by test code
#


def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % (
        multiprocessing.current_process().name,
        func.__name__, args, result
    )


def calculatestar(args):
    return calculate(*args)


def mul(a, b):
    time.sleep(3)
    return a * b


def work(cmd):
    return subprocess.run(cmd, shell=True)


def run_subprocess(func, args):
	print("Func is", func, "Arg is", args)
	func(args)
	return f"Current subprocess {multiprocessing.current_process().name} starts at {datetime.now()}"


def run_subprocess_star(args):
    return run_subprocess(*args)


def test():
    PROCESSES = 4
    print('Creating pool with %d processes\n' % PROCESSES)

    with multiprocessing.Pool(PROCESSES) as pool:
        # TASKS = [(mul, (i, 7)) for i in range(4)]
        TASKS = [(work, "python async_subprocess.py") for _ in range(4)]

        print(TASKS)

        print('Running commands using pool.map() --- will block till complete:')
        for _ in pool.map(run_subprocess_star, TASKS):
            pass
        # for x in pool.map(calculatestar, TASKS):
        #     print('\t', x)
        # print()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    test()
