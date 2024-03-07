from multiprocessing import Process, current_process, RLock, Value, Array
from ctypes import c_int, c_double, Structure, c_char
from sys import exit


class Point(Structure):
    _fields_ = [("x", c_double), ("y", c_double)]


def worker(value: Value, string: Array, arr: Array):
    print(f" Start process {current_process().name}")
    with value.get_lock():
        value.value += 1
    with string.get_lock():
        string.value = b"Good morning"
    with arr.get_lock():
        for point in arr:
            point.x += value.value
            point.y += value.value

    exit(0)


if __name__ == "__main__":

    value = Value(c_double, 1.5, lock=RLock())
    string = Array(c_char, b"Good evening", lock=RLock())
    arr = Array(Point, [(0, 0), (2, 0), (3, 3)], lock=RLock())

    process = []
    for i in range(3):
        t = Process(target=worker, args=(value, string, arr))
        process.append(t)
        t.start()

    [pr.join() for pr in process]

    [print(pr.exitcode) for pr in process]
    print(value.value)
    print(string.value)
    [print(point.x, point.y) for point in arr]

