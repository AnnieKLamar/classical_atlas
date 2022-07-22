import requests
import json
import gzip
import shutil
import os


def wget_url(url):
    """
    Downloads the file at the given URL and returns the file name.

    Keyword arguments:
    url -- the URL from which to download the file (required)

    Returns:
    (string) file name of downloaded file
    """
    response = requests.get(url)
    open(url.split("/")[-1], "wb").write(response.content)
    return url.split("/")[-1]

def unzip_gz(file):
    """
    Unzips the provided .gz file and returns the unzipped file.

    Keyword arguments:
    file -- the .gz file (required)

    Returns:
    (string) file name of unzipped file
    """
    new_name = file[:-3]
    with gzip.open(file, 'rb') as f_in:
        with open(new_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    f_in.close()
    #os.remove(file)
    f_out.close()
    return file[:-3]
    
def get_file(url):
    """
    Downloads, unzips, and returns the file at the given URL.

    Keyword arguments:
    url -- the URL from which to access the data (required)

    Returns:
    (string) file name
    """
    file = wget_url(url)
    if file.endswith(".gz"):
        file = unzip_gz(file)
    return file

def get_df(json_file):
    """
    Opens the provided JSON file and loads it into a dataframe.

    Keyword arguments:
    json_file -- string name of JSON file with data to be loaded

    Returns:
    (list) dataset as list of dictionaries
    """
    json_file = open(json_file, "r+", encoding="utf8")
    df = json.load(json_file)
    return df
        
def get_data(url):
     """
     Downloads, unzips, and loads the JSON file at the given URL.

     Keyword arguments:
     url -- web location.py of the JSON file from which to download data

     Returns:
     (list) dataset with JSON file data, list of dictionaries
     """
     return get_df(get_file(url))