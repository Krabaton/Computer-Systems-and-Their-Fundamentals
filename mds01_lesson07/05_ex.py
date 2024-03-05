import logging
from threading import Thread, current_thread, Event
from time import sleep
from random import randint


def master(e: Event):
    logging.info("master is working")
    sleep(randint(1, 2))
    logging.info("master finished")
    e.set()


def worker(e: Event):
    logging.info(f"{current_thread().name} waiting")
    e.wait()
    logging.info(f"{current_thread().name} is working")
    sleep(randint(1, 2))
    logging.info(f"{current_thread().name} finished")


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    event = Event()

    m = Thread(target=master, args=(event,))

    for i in range(3):
        t = Thread(target=worker, args=(event,))
        t.start()

    m.start()
