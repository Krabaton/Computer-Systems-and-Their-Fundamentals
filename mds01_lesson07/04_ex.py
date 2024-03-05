import logging
from threading import Thread, current_thread, RLock
from time import sleep
from random import randint

count = 0
lock = RLock()

def worker():
    global count
    while True:
        sleep(randint(0, 2))
        # lock.acquire()
        with lock:
            count += 1
            with open('test.txt', 'a') as f:
                f.write(f'{current_thread().name} {count}\n')
        # lock.release()


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    for i in range(3):
        t = Thread(target=worker,)
        t.start()


