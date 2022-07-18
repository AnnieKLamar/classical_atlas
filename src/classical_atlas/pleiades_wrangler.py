"""
Classical Atlas

@author: kalamar
"""
import downloaders

def make_Pleiades_objects (data_level = 'basic', download_latest_data=False):
    if download_latest_data:
        data = downloaders.get_pleiades_data("http://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz")
    else:
        raw_data_file = downloaders.unzip_gz("data/pleiades_data.json")
        data = downloaders.get_df(raw_data_file)
        