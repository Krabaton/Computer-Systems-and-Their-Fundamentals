import logging
from multiprocessing import Pool, current_process, cpu_count
from time import sleep
from random import randint

format = "%(processName)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def worker(val):
    return val ** 2


if __name__ == "__main__":

    print(f"CPUs: {cpu_count()}")

    with Pool(3) as pool:
        result = pool.map(worker, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        logging.info(result)

        iterator = pool.imap(worker, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        print(iterator)
        print(next(iterator))
        print(iterator.next())
        for i in iterator:
            logging.info(i)

    print(f"End of process {current_process().name}")
