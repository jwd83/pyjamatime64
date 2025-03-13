import csv
import os
import sys


def main():
    # check if the argument is a file that exists
    path = sys.argv[1]

    rows = load_csv(path)
    print(len(rows))

    for row in rows:
        print(row["name"])


def load_csv(path: str, header_row: int = 1) -> list | bool:

    rows = []

    # check if the path exists
    if not os.path.exists(path):
        print(f"Error: Supplied path does not exist: {path}")
        return False

    # check if the path is a file
    if not os.path.isfile(path):
        print(f"Error: Supplied path is not a file: {path}")
        return False

    # open the CSV as a DictReader
    with open(path, "r") as f:
        # skip rows if header_row is greater than 1
        if header_row > 1:
            for _ in range(header_row - 1):
                f.readline()

        # Check for multiple comment lines
        while True:
            comment_check_position = f.tell()
            comment_check = f.readline().strip()
            if not comment_check.startswith("#"):
                f.seek(comment_check_position)
                break
            else:
                print(f"Comment: {comment_check}")

        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows


if __name__ == "__main__":
    main()
