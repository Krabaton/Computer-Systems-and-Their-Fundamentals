import argparse
import logging
from pathlib import Path
from shutil import copyfile
from multiprocessing import Process, current_process
from sys import exit

format = "%(processName)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

parser = argparse.ArgumentParser(description="Sorting files")
parser.add_argument("--source", "-s", required=True, help="Source dir")
parser.add_argument("--output", "-o", help="Output dir", default="destination")
args = vars(parser.parse_args())

source = Path(args["source"])
output = Path(args["output"])


def get_folders(path: Path) -> None:
    logging.info(f"Getting folders from {path} - {current_process().name}")
    for file in path.iterdir():
        if file.is_dir():
            inner_process = Process(target=get_folders, args=(file,))
            inner_process.start()
        else:
            copy_file(file)


def copy_file(file: Path):
    folder = output / file.suffix[1:]
    try:
        folder.mkdir(exist_ok=True, parents=True)
        copyfile(file, folder / file.name)
    except OSError as e:
        logging.error(e)
        exit(1)


def copy_files(path: Path):
    for file in path.iterdir():
        if file.is_file():
            copy_file(file)


if __name__ == "__main__":

    pr = Process(target=get_folders, args=(source,))
    pr.start()
    pr.join()

    print(f"All files copied to {output}. Source dir will be deleted")
