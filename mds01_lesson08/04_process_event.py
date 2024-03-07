import logging
from multiprocessing import Process, current_process, Event
from time import sleep
from random import randint

format = "%(processName)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def master(e: Event):
    logging.info("master is working")
    sleep(randint(1, 2))
    logging.info("master finished")
    e.set()


def worker(e: Event):
    logging.info(f"{current_process().name} waiting")
    e.wait()
    logging.info(f"{current_process().name} is working")
    sleep(randint(1, 2))
    logging.info(f"{current_process().name} finished")


if __name__ == "__main__":

    event = Event()

    m = Process(target=master, args=(event,))

    for i in range(3):
        t = Process(target=worker, args=(event,))
        t.start()

    m.start()
