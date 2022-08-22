import json
import os
from bs4 import BeautifulSoup
import csv
from collections import defaultdict


def load_json(file_name):
    """
    Load a JSON file as a Python dataframe.

    Parameters
    ----------
    file_name : string
        file name of the target JSON file

    Returns
    -------
    dataframe
        A dataframe representing the JSON file
    """
    file = open(file_name, "r+", encoding="utf8")
    df = json.load(file)
    return df


def get_topos_data():
    """
    Loads the Topos Text Gazeteer data.

    Returns
    -------
    dataframe
        A dataframe with data from the Topos Text Gazeteer
    """
    return load_json("data/ToposTextGazetteer.jsonld")


def switch_to_pleiades_ids(topos_df, topos_places):
    """
    Swap all IDs to Pleiades IDs if possible

    Parameters
    ----------
    topos_df : dataframe
        a dataframe with data from the Topos Text Gazeteer

    topos_places : dictionary
        a dictionary with key=texts and value=list of Topos Text IDs

    Returns
    -------
    dictionary
        dictionary with key=texts and value=list of Pleiades IDs, where possible

    Notes
    -----
    This method reports how many IDs were unable to be switched. In the case that there is no
    corresponding Pleiades ID for a given Topos Text ID, the Topos Text ID is retained in the dictionary.
    """
    ids = _topos_pleiades_ids(topos_df)
    switch_counter = 0
    did_not_switch = 0
    for place in topos_places.keys():
        for i in range(len(topos_places[place])):
            topos_id = topos_places[place][i]
            if topos_id in ids.keys():
                topos_places[place][i] = ids[topos_id]
                switch_counter += 1
            else:
                did_not_switch += 1
    print("Made " + str(switch_counter) + " switches.")
    print("No Pleiades ID available for " + str(did_not_switch) + " topos places.")
    return topos_places


def swap_key_value_pairs(textual_refs):
    """
    Reorganize the dictionary with key=ID and value= list of texts

    Parameters
    ----------
    textual_refs : dictionary
        dictionary with key=text and value=ID

    Returns
    -------
    dictionary
        dictionary with key=ID and value=list of texts
    """
    reorganized = defaultdict(list)
    for text in textual_refs.keys():
        for id in textual_refs[text]:
            reorganized[id].append(text)
    for i in reorganized.keys():
        set(reorganized[i])
    return reorganized


def parse_topos_place_refs():
    """
    Create a dictionary from the Topos Text .csv file

    Returns
    -------
    dictionary
        A dictionary with key=text and value=list of Topos Text IDs
    """
    topos_places = defaultdict(list)
    with open('data/topos_data.csv', 'r', encoding="utf8") as topos_csv:
        csv_reader = csv.reader(topos_csv, delimiter=',')
        for row in csv_reader:
            if len(row) > 0:
                for i in range(len(row)):
                    if i == 0:
                        key = row[i]
                        topos_places[key] = []
                    else:
                        topos_places[key].append(row[i])
    return topos_places


def _parse_topos_place_refs_from_all_files(data='data/topos_data/'):
    directory = os.fsencode(data)
    topos_places = defaultdict(list)
    print("Parsing data...please be patient.")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # print(filename)
        if filename.endswith(".htm") or filename.endswith(".html"):
            # print("here!")
            name = "data/topos_data/" + filename
            text = open(name, "r", encoding="utf8").read()
            soup = BeautifulSoup(text, 'html.parser')
            title = soup.find('meta', property='dc:title', itemprop='name', lang='en').get_text("|")
            elements = title.split("|")
            for element in elements:
                if len(element) > 1:
                    short_title = element
                    # print(short_title)
                    break
            place_refs = soup.find_all('a', {"class": "place"})
            for ref in place_refs:
                link = ref['about'].split("/")[-1]
                topos_places[short_title].append(link)
        else:
            continue
    print("Parsed " + str(len(topos_places)) + " documents.")
    return topos_places


def _write_topos_place_refs_to_csv(topos_place_refs):
    with open('data/topos_data.csv', 'w+', encoding="utf8") as topos_csv:
        # create the csv writer
        writer = csv.writer(topos_csv)
        for item in topos_place_refs.keys():
            row = [item]
            for ref in topos_place_refs[item]:
                row.append(ref)
            writer.writerow(row)


def _topos_pleiades_ids(df, key_selector='topos'):
    topos_pleiades_ids = {}
    pleiades_topos_ids = {}
    for location in range(len(df['features'])):
        pleiades_link = None
        pleiades_id = None
        if 'links' in df['features'][location]:
            if df['features'][location]['links'][0]:
                pleiades_link = df['features'][location]['links'][0]['identifier']
        topos_link = df['features'][location]['@id']
        if pleiades_link and 'pleiades' in pleiades_link:
            pleiades_id = pleiades_link.split("/")[-1]
        topos_id = topos_link.split("/")[-1]
        topos_pleiades_ids[topos_id] = pleiades_id
        if pleiades_id:
            pleiades_topos_ids[pleiades_id] = topos_id
    if key_selector == 'topos':
        return topos_pleiades_ids
    else:
        return pleiades_topos_ids