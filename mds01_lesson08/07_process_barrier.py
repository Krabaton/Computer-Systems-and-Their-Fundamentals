import logging
from multiprocessing import Process, Barrier, current_process
from time import sleep
from random import randint

format = "%(processName)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def worker(b: Barrier):
    name = current_process().name
    logging.info("waiting...")
    num = b.wait()
    sleep(1)
    logging.info(f"{name}:{num}")


if __name__ == "__main__":

    br = Barrier(5)

    for i in range(10):
        th = Process(target=worker, args=(br,))
        th.start()
