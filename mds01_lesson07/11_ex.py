import logging
from threading import Thread, Semaphore, RLock, current_thread
from time import sleep
from random import randint


class Logger:
    def __init__(self):
        self.active = []
        self.lock = RLock()

    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            logging.info(f"Active thread {name}. Pool: {self.active}")

    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.info(f"Inactive thread {name}. Pool: {self.active}")


def worker(s: Semaphore, log: Logger):
    logging.info("waiting...")
    with s:
        name = current_thread().name
        logging.info("Got semaphore!")
        log.make_active(name)
        sleep(randint(0, 2))
        logging.info("done")
        log.make_inactive(name)


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    pool = Semaphore(3)
    logger = Logger()

    for i in range(15):
        th = Thread(target=worker, args=(pool, logger))
        th.start()
