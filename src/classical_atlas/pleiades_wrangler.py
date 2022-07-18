"""
Classical Atlas

@author: kalamar
"""
import downloaders
from pleiad import Pleiad


def make_pleiades_objects(download_latest_data=False):
    if download_latest_data:
        print("Warning: Pleiades data files are large and may require considerable time to download.")
        input("Press Enter to continue...")
        data = downloaders.get_pleiades_data("http://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz")
    else:
        raw_data_file = downloaders.unzip_gz("data/pleiades_data.json")
        data = downloaders.get_df(raw_data_file)
    pleiades = []
    for row in range(len(data)):
        pleiades.append(Pleiad(data[row]))
    print(pleiades[1])


def main():
    make_pleiades_objects()


if __name__ == "__main__":
    main()