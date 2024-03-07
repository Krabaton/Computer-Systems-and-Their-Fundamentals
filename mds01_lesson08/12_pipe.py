import sys
from multiprocessing import Pipe, Process


def worker(conn: Pipe, name: str):
    val = conn.recv()
    print(f"{name} received {val}")
    sys.exit(0)


if __name__ == "__main__":
    first_conn1, second_conn1 = Pipe(duplex=False)
    first_conn2, second_conn2 = Pipe(duplex=False)

    first_pr = Process(target=worker, args=(first_conn1, "first"))
    second_pr = Process(target=worker, args=(first_conn2, "second"))

    first_pr.start()
    second_pr.start()

    print("Sending 42")

    second_conn1.send(42)
    second_conn2.send(23)
