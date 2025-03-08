# load asset_sources.csv into a dictionary

# make sure that all asset sources and files in the asset folder are accounted for.
# print any mismatches

import csv
import os


def main():
    asset_sources = load_asset_sources()
    print(asset_sources)


def load_asset_sources():
    asset_sources = {}

    # create a CSV reader that uses the first row as keys
    with open("asset_sources.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            asset_sources[row["file"]] = row

    return asset_sources


if __name__ == "__main__":
    main()
