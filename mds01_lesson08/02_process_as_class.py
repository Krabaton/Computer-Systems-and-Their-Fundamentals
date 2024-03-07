import logging
from multiprocessing import Process, current_process
from time import sleep
from random import randint

m = "test"

format = "%(processName)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


class MyProcess(Process):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, args=args, kwargs={}, daemon=daemon)
        self.args = args

    def run(self):
        logging.info("Starting " + current_process().name)
        ttl = randint(1, 3)
        sleep(ttl)
        logging.info(m)
        logging.info("Exiting " + current_process().name + ' ttl: ' + str(ttl))


if __name__ == "__main__":

    process = []
    for i in range(3):
        t = MyProcess(args=(f'Thread-{i}',), daemon=True)
        process.append(t)
        t.start()

    # for t in process:
    #     t.join()

    sleep(1.5)
    print('Main thread exiting.')
