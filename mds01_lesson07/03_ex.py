import logging
from threading import Timer
from time import sleep


def worker(name):
    logging.info('Starting')
    logging.info(f"{name} is running")
    logging.info('Exiting')


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    t1 = Timer(0.5, worker, args=(f'Thread-0.5',))
    t1.name = "New name"
    t1.start()

    t2 = Timer(1.5, worker, args=(f'Thread-1.5',))
    t2.start()

    sleep(1)
    t1.cancel()
    t2.cancel()
    print('Main thread exiting.')
