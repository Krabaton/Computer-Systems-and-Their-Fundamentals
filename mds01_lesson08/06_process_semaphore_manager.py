import logging
from multiprocessing import Process, Semaphore, Manager, current_process
from time import sleep
from random import randint

format = "%(processName)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def worker(s: Semaphore, data: dict):
    logging.info("waiting...")
    with s:
        logging.info("Got semaphore!")
        ttl = randint(0, 2)
        sleep(ttl)
        # data.append(ttl)
        data[current_process().name] = ttl
        logging.info("done")


if __name__ == "__main__":
    pool = Semaphore(3)
    with Manager() as m:
        data = m.dict()
        # data = m.list()
        print(data)

        process = []
        for i in range(10):
            pr = Process(target=worker, args=(pool, data))
            pr.start()
            process.append(pr)

        [pr.join() for pr in process]
        print(data)
