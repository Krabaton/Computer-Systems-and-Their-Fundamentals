from multiprocessing import Process, RLock as PRLock
from threading import Thread, RLock as TRLock
from multiprocessing.dummy import Pool, RLock as DRLock
from time import time


def worker(values, filename, lock):
    with lock:
        with open(filename, 'a') as f:
            for value in values:
                f.write(f'{value ** 2}\n')


if __name__ == '__main__':
    values = list(range(600_001))

    th_lock = TRLock()
    th_filename = 'th.txt'
    threads = [
        Thread(target=worker, args=(values[:200_000], th_filename, th_lock)),
        Thread(target=worker, args=(values[200_000:400_000], th_filename, th_lock)),
        Thread(target=worker, args=(values[400_000:], th_filename, th_lock)),
    ]
    timer = time()
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    print(f'Elapsed time Threads: {round(time() - timer, 4)}')

    pr_lock = PRLock()
    pr_filename = 'pr.txt'
    processes = [
        Process(target=worker, args=(values[:200_000], pr_filename, pr_lock)),
        Process(target=worker, args=(values[200_000:400_000], pr_filename, pr_lock)),
        Process(target=worker, args=(values[400_000:], pr_filename, pr_lock)),
    ]
    timer = time()
    [process.start() for process in processes]
    [process.join() for process in processes]
    print(f'Elapsed time Process: {round(time() - timer, 4)}')

    dr_lock = DRLock()
    dr_filename = 'dr.txt'
    with Pool(3) as pool:
        timer = time()
        pool.starmap(worker, [(values[:200_000], dr_filename, dr_lock),
                              (values[200_000:400_000], dr_filename, dr_lock),
                              (values[400_000:], dr_filename, dr_lock)])
        print(f'Elapsed time Dummy Process: {round(time() - timer, 4)}')

    timer = time()
    worker(values, 'native.txt', dr_lock)
    print(f'Elapsed time: {round(time() - timer, 4)}')
