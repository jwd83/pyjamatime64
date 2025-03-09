# load asset_sources.csv into a dictionary

# make sure that all asset sources and files in the asset folder are accounted for.
# print any mismatches

"""
asset_sources.csv snippet:

path,source,url source,url page
assets/textures/cobe.jpg,NASA Public Domain,https://lambda.gsfc.nasa.gov/product/cobe/more_images/cobeslide28.jpg,https://lambda.gsfc.nasa.gov/product/cobe/cobe_image_table.html
assets/textures/wmap.png,NASA Public Domain,https://map.gsfc.nasa.gov/media/121238/ilc_9yr_moll4096BW.png,https://map.gsfc.nasa.gov/media/121238/index.html
assets/textures/wmap-sphere.png,NASA Public Domain,https://lambda.gsfc.nasa.gov/product/wmap/dr4/sos/7year/ilc/wmap_ilc_7yr_v4_200uK_RGB_sos.png,https://lambda.gsfc.nasa.gov/product/wmap/dr4/sos/7year/

"""


import csv
import os


def main():
    asset_sources = load_asset_sources()
    # print(asset_sources)
    missing_sources = []
    missing_files = []
    sourced_files = []

    # recursively walk the asset folder
    for root, dirs, files in os.walk("assets"):
        for file in files:
            path = os.path.join(root, file)

            # normalize the path
            path = path.replace("\\", "/")

            if path not in asset_sources:
                missing_sources.append(path)
            else:
                sourced_files.append(path)
                del asset_sources[path]

    # print any remaining asset sources
    for path in asset_sources:
        missing_files.append(path)

    # generate a summary
    print(f"\nProperly sourced asset files ({len(sourced_files)}):")
    for path in sourced_files:
        print(path)
    print(f"\nFiles missing sources ({len(missing_sources)}):")
    for path in missing_sources:
        print(path)
    print(f"\nSources missing files ({len(missing_files)}):")
    for path in missing_files:
        print(path)


def load_asset_sources():
    asset_sources = {}

    # create a CSV reader that uses the first row as keys
    with open("asset_sources.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            asset_sources[row["path"]] = row

    return asset_sources


if __name__ == "__main__":
    main()
