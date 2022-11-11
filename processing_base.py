from typing import Any
# multiprocessing
from multiprocessing import Process
# multithreading
from threading import Thread, local
from requests.sessions import Session
from queue import Queue


class CPUTaskSupports:
    # multiprocessing
    jobs = []
    NUM_PROCESSES = 50_000
    # multithreading
    queue = Queue(maxsize=0)
    thread_local = local()
    thread_num = 10

    def get_session(self) -> Session:
        if not hasattr(self.thread_local, "session"):
            # Create a new Session if not exists
            self.thread_local.session = Session()
        return self.thread_local.session

    def multiprocess_jobs(self, target_args: tuple[Any, ...], target_function: Any):
        i = 0
        while i < self.NUM_PROCESSES - 1:
            process = Process(target=target_function, args=target_args)
            i += 100
            self.jobs.append(process)

        for j in self.jobs:
            try:
                j.start()
            except Exception as err:
                f = open("multiprocessing_jobs.log", "a")
                f.write(err)
                f.close()

        for j in self.jobs:
            j.join()

    def multithread_process(self, items: list[Any], target_function: Any) -> None:
        for item in items:
            self.queue.put(item)

        for _ in range(self.thread_num):
            t_worker = Thread(target=target_function)
            t_worker.daemon = True
            t_worker.start()

        self.queue.join()
