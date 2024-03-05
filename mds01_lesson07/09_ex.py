import logging
from threading import Thread, current_thread, Condition
from time import sleep
from random import randint


def master(c: Condition):
    logging.info("master is working")
    sleep(randint(1, 2))
    with c:
        logging.info("master finished")
        c.notify_all()


def worker(c: Condition):
    logging.info(f"{current_thread().name} waiting")
    with c:
        c.wait()
        logging.info(f"{current_thread().name} is working")
        sleep(randint(1, 2))
        logging.info(f"{current_thread().name} finished")


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    cond = Condition()

    m = Thread(target=master, args=(cond,))

    for i in range(3):
        t = Thread(target=worker, args=(cond,))
        t.start()

    m.start()
