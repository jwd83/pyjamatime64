import csv
import os
import sys


def main():
    # check if the argument is a file that exists
    file_path = sys.argv[1]

    # check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        sys.exit(1)

    # check if the file is a file
    if not os.path.isfile(file_path):
        print(f"{file_path} is not a file.")
        sys.exit(1)

    rows = load_csv(file_path)
    print(len(rows))

    for row in rows:
        print(row["name"])


def load_csv(path: str):
    rows = []

    # open the CSV as a DictReader with first row as keys

    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows


if __name__ == "__main__":
    main()
