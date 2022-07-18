"""
Classical Atlas
module header
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
        raw_data_file = downloaders.unzip_gz("data/pleiades-places-latest.json.gz")
        data = downloaders.get_df(raw_data_file)
    data = data['@graph']
    pleiades = []
    for row in range(len(data)):
        pleiades.append(Pleiad(data[row]))
    return pleiades


def main():
    pleiades = make_pleiades_objects()
    test1 = pleiades[21]
    #test2 = pleiades[5]
    test3 = pleiades[31]
    #test1.full_report()
    #test2.full_report()
    #test3.full_report()
    for n in test3.names:
        n.name_summary()

if __name__ == "__main__":
    main()