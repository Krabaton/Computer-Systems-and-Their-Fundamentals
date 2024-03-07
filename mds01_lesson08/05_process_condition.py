import logging
from multiprocessing import Process, current_process, Condition
from time import sleep
from random import randint

format = "%(processName)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def master(c: Condition):
    logging.info("master is working")
    sleep(randint(1, 2))
    with c:
        logging.info("master finished")
        c.notify_all()


def worker(c: Condition):
    logging.info(f"{current_process().name} waiting")
    with c:
        c.wait()
        logging.info(f"{current_process().name} is working")
        sleep(randint(1, 2))
        logging.info(f"{current_process().name} finished")


if __name__ == "__main__":


    cond = Condition()

    m = Process(target=master, args=(cond,))

    for i in range(3):
        t = Process(target=worker, args=(cond,))
        t.start()

    m.start()