import argparse
import logging
from pathlib import Path
from shutil import copyfile
from multiprocessing import Pool, cpu_count

format = "%(processName)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

parser = argparse.ArgumentParser(description="Sorting files")
parser.add_argument("--source", "-s", required=True, help="Source dir")
parser.add_argument("--output", "-o", help="Output dir", default="destination")
args = vars(parser.parse_args())

source = Path(args["source"])
output = Path(args["output"])


def get_folders(path: Path) -> list[Path]:
    folders = []
    for file in path.iterdir():
        if file.is_dir():
            folders.append(file)
            inner_folders = get_folders(file)
            if len(inner_folders) > 0:
                folders = folders + inner_folders
    return folders


def copy_files(path: Path):
    for file in path.iterdir():
        if file.is_file():
            folder = output / file.suffix[1:]
            try:
                folder.mkdir(exist_ok=True, parents=True)
                copyfile(file, folder / file.name)
            except OSError as e:
                logging.error(e)


if __name__ == "__main__":

    folders = [source, *get_folders(source)]  # folders = [source] + get_folders(source)
    print(folders)

    with Pool(processes=cpu_count()) as pool:
        pool.map(copy_files, folders)
        pool.close()
        pool.join()

    print(f"All files copied to {output}. Source dir will be deleted")
