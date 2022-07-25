"""Contains methods to download and unzip JSON files.
"""

import requests
import json
import gzip
import shutil


def wget_url(url):
    """Download the file at the given URL and return the file name.

    Parameters
    ----------
    url : string
        The URL from which to download the file

    Returns
    -------
    string
        file name of downloaded file
    """
    response = requests.get(url)
    open(url.split("/")[-1], "wb").write(response.content)
    return url.split("/")[-1]


def unzip_gz(file):
    """Unzip the provided .gz file and return the unzipped file.

    Parameters
    ----------
    file : string
        Name of the .gz file

    Returns
    -------
    string
        Filename of the unzipped file
    """
    new_name = file[:-3]
    with gzip.open(file, 'rb') as f_in:
        with open(new_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    f_in.close()
    f_out.close()
    return file[:-3]


def get_file(url):
    """Download, unzip, and return the file at the given URL.

    Parameters
    ----------
    url : string
        The URL from which to access the data (required)

    Returns
    -------
    string
        Name of the downloaded file
    """
    file = wget_url(url)
    if file.endswith(".gz"):
        file = unzip_gz(file)
    return file


def get_df(json_file):
    """Open the provided JSON file and load it into a dataframe.

    Parameters
    ----------
    json_file : string
        String name of JSON file with data to be loaded

    Returns
    -------
    list
        dataset as list of dictionaries
    """
    json_file = open(json_file, "r+", encoding="utf8")
    df = json.load(json_file)
    return df


def get_data(url):
    """Download, unzip, and load the JSON file at the given URL.

    Parameters
    ----------
    url : string
        Web location.py of the JSON file from which to download data

    Returns
    -------
    list
        Dataset with JSON file data as list of dictionaries
    """
    return get_df(get_file(url))