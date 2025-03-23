import csv
import os
import sys


def main():
    # check if the argument is a file that exists
    path = sys.argv[1]

    rows = load(path)
    print(len(rows))

    for row in rows:
        print(row["name"])


# returns a list of rows that match the property and value
# limit is the maximum number of rows to return
# if limit is 1, the first row that matches is returned directly


def prop_eq(data: list, property: str, value: any, limit: int = 0):
    """search for a property in a list of dictionaries, like those returned by load().

    Args:
        data (list): the data to search
        property (str): the property to examine
        value (any): the value to search for
        limit (int, optional): maximum results to return. if set to 1 return the first result directly.

    Returns:
        list | dict: a list of results or a single result if limit is 1
    """
    results = []

    if limit < 0:
        print("pcsv -> Warning: Limit should be greater than or equal to 0")
        return results

    if limit == 1:
        for row in data:
            if row[property] == value:
                return row
    else:

        for row in data:
            if row[property] == value:
                results.append(row)
            if limit > 0 and len(results) >= limit:
                break

        return results


def load(path: str, header_row: int = 1, skip_comments: bool = True) -> list | bool:

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
        if skip_comments:
            while True:
                comment_check_position = f.tell()
                comment_check = f.readline().strip()
                if not comment_check.startswith("#"):
                    f.seek(comment_check_position)
                    break
                else:
                    print(f"Header comment: {comment_check}")

        reader = csv.DictReader(f)
        for row in reader:
            add_row = True
            for _, value in row.items():
                first_item = value.strip()
                if first_item.startswith("#"):
                    add_row = False
                    print(f"Data comment: {value}")
                break
            if add_row:
                rows.append(row)

    return rows


if __name__ == "__main__":
    main()
