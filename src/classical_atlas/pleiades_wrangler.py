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
    test2 = pleiades[5]
    test3 = pleiades[31]
    print(test1.type)
    print(test2.type)
    print(test3.type)
    # test1.report(detail='long')
    # for n in test1.locations:
    #     n.report(detail='long')
    #
    # test3.report(detail='long')
    # for n in test3.locations:
    #     n.report(detail='long')

if __name__ == "__main__":
    main()