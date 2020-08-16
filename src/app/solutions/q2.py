import time
from multiprocessing import Process, Queue, Pool, Lock


class QueueFun():

    def __init__(self):
        self.lock = Lock()

    def writing_queue(self, work_tasks):
        count = 0
        for i in range(0 , 10):
            self.lock.acquire()
            count = count + 1
            self.lock.release()
            print("Writing to queue")
            if count == 3 :
                break
            work_tasks.put(1)

    def read_queue(self, work_tasks):
        for i in range(0, 2):
            print('Reading from queue')
            work_tasks.get()


if __name__ == '__main__':
    q = QueueFun()
    work_tasks = Queue()

    write_process = Process(target=q.writing_queue,
                            args=(work_tasks,))
    write_process.start()

    processes = []
    for i in range(0, 1):
        processes.append(Process(target=q.read_queue,
                                 args=(work_tasks,)))

    for p in processes:
        p.start()

    write_process.join()
    for p in processes:
        p.join()

