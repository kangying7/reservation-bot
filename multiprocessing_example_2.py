from multiprocessing import Process, Manager
import os


def child_task(results_dict, x, y):
    # the child task spawns new tasks
    p1 = Process(target=grandchild_task, args=(results_dict, x))
    p1.start()
    pid1 = p1.pid
    p2 = Process(target=grandchild_task, args=(results_dict, y))
    p2.start()
    pid2 = p2.pid
    p1.join()
    p2.join()
    pid = os.getpid()
    results_dict[pid] = results_dict[pid1] + results_dict[pid2]



def grandchild_task(results_dict, n):
    pid = os.getpid()
    results_dict[pid] = n * n


def main():
    manager = Manager()
    results_dict = manager.dict()
    p = Process(target=child_task, args=(results_dict, 2, 3))
    p.start()
    pid = p.pid
    p.join()
    # results will be stored with key p.pid:
    print(results_dict[pid])

if __name__ == '__main__':
    main()