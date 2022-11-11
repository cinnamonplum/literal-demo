import csv
from typing import List


def write_to_txt(filename: str, *args: str) -> None:
    """
    Util for spaced printing of n number of arguments
    """
    with open(filename, "a") as out:
        for param in args:
            out.write(param)
            out.write("\n")

        out.write("\n\n")
        out.close()


def write_to_csv(filename: str, fieldnames: List[str], values: dict) -> None:
    """
    Util for printing out dictionary values to a csv file
    """

    with open(filename, "a", newline="") as out:
        _writer = csv.DictWriter(out, fieldnames=fieldnames, )
        _writer.writerow(values)
