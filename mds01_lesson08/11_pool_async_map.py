import logging
from multiprocessing import Pool, current_process, cpu_count
from time import sleep
from random import randint

format = "%(processName)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def worker(val):
    return val ** 2


def get_results(results):
    logging.info(results)


if __name__ == "__main__":
    print(f"CPUs: {cpu_count()}")

    with Pool(cpu_count()) as pool:
        pool.map_async(worker, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], callback=get_results)
        pool.close()
        pool.join()

    print(f"End of process {current_process().name}")
