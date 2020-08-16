import time
from multiprocessing import Process, Queue, Pool


class QueueFun():

    def writing_queue(self, work_tasks):
        while True:
            print("Writing to queue")
            work_tasks.put(1)
            time.sleep(1)

    def read_queue(self, work_tasks):
        while True:
            print('Reading from queue')
            work_tasks.get()
            time.sleep(2)


if __name__ == '__main__':
    q = QueueFun()
    work_tasks = Queue()

    write_process = Process(target=q.writing_queue,
                                     args=(work_tasks,))
    write_process.start()

    for i in range(0 , 3):
        read_process = Process(target=q.read_queue,
                                         args=(work_tasks,))
        print('Starting read_process' , i)
        read_process.start()
        read_process.join()

    write_process.join()


