import logging
from threading import Thread, current_thread, Event
from time import sleep
from random import randint


def worker(e: Event, e_exit: Event):
    while True:
        if e_exit.is_set():
            break

        if e.is_set():
            continue
        else:
            logging.info(f"{current_thread().name} working")
            sleep(1)
    logging.info(f"{current_thread().name} done")


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    event = Event()
    event_exit = Event()

    th = Thread(target=worker, args=(event, event_exit))
    th.start()

    logging.info("Start")
    sleep(2.1)
    event.set()
    logging.info("Wait")
    sleep(2)
    event.clear()
    logging.info("Start")
    sleep(3)
    event_exit.set()
    logging.info("End")


