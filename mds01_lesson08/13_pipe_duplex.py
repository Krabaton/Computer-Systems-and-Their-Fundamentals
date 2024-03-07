import sys
from multiprocessing import Pipe, Process


class Baz:
    def __init__(self, name):
        self.name = name


def worker(conn: Pipe):
    while True:
        try:
            instance = conn.recv()
            print(f"received {instance}")
            conn.send(f"Instance: {instance}")
        except EOFError:
            return None


def sender(conn: Pipe, store: list):
    for i in store:
        conn.send(i)
        print(conn.recv())


if __name__ == "__main__":
    start, end = Pipe()
    baz = Baz("baz")
    store = [42, "Hello World", baz, baz.name, None, 42, {"foo": "bar"}]

    p_sender = Process(target=sender, args=(end, store))
    p2 = Process(target=worker, args=(start,))

    p_sender.start()
    p2.start()

    p_sender.join()
    start.close()
    end.close()
