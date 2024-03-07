import logging
from multiprocessing import Pool, current_process, cpu_count
from time import sleep
from random import randint

format = "%(processName)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def worker():
    name = current_process().name
    logging.info("waiting...")
    ttl = randint(1, 3)
    sleep(ttl)
    logging.info(f"{name}: {ttl}")
    return {"name": name, "ttl": ttl}


if __name__ == "__main__":

    print(f"CPUs: {cpu_count()}")

    with Pool(cpu_count()) as pool:
        for _ in range(cpu_count()):
            pool.apply_async(worker, callback=lambda x: logging.info(x))
        pool.close()
        pool.join()  # pool.terminate()

    print(f"End of process {current_process().name}")
