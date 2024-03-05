import logging
from threading import Thread, Barrier, current_thread
from time import sleep
from random import randint


def worker(b: Barrier):
    name = current_thread().name
    logging.info("waiting...")
    num = b.wait()
    sleep(1)
    logging.info(f"{name}:{num}")


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    br = Barrier(5)

    for i in range(10):
        th = Thread(target=worker, args=(br,))
        th.start()
