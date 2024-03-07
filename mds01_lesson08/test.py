import multiprocessing


def demo(argument):
    print(argument)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")  # Changing this to "fork" (on platforms where it is
    # available) can also cause the below code to work.

    process = multiprocessing.Process(target=demo, args=[multiprocessing.Value("i", 0)])  # FAILS

    # process=multiprocessing.Process(target=demo, args=[0])                            # WORKS

    # reference_To_Number=multiprocessing.Value("i", 0)                                 # WORKS
    # process=multiprocessing.Process(target=demo, args=[reference_To_Number])

    process.start()
    process.join()
