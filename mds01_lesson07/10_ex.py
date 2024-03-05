import logging
from threading import Thread, Semaphore
from time import sleep
from random import randint


def worker(s: Semaphore):
    logging.info("waiting...")
    with s:
        logging.info("Got semaphore!")
        sleep(randint(0, 2))
        logging.info("done")


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    pool = Semaphore(3)

    for i in range(15):
        th = Thread(target=worker, args=(pool,))
        th.start()
