import logging
from threading import Thread, current_thread
from time import sleep
from random import randint

m = "test"

class MyThreads(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self.args = args

    def run(self):
        logging.info("Starting " + current_thread().name)
        ttl = randint(1, 3)
        sleep(ttl)
        logging.info(m)
        logging.info("Exiting " + current_thread().name + ' ttl: ' + str(ttl))


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    threads = []
    for i in range(3):
        t = MyThreads(args=(f'Thread-{i}',), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    sleep(1.5)
    print('Main thread exiting.')
