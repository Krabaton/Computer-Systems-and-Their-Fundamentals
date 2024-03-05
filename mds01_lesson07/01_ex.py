from threading import Thread


def worker(name):
    print('Starting')
    print(f"{name} is running")
    print('Exiting')


if __name__ == '__main__':
    for i in range(3):
        t = Thread(target=worker, args=(f'Thread-{i}',))
        t.start()
