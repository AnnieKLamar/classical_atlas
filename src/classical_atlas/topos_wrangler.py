import json
import os
from bs4 import BeautifulSoup
from pathlib import Path

topos_gaz = "data/topos_data/topos_text_gazeteer.jsonld"


def load_json(file_name):
    file = open(file_name, "r+", encoding="utf8")
    df = json.load(file)
    return df


def topos_pleiades_ids(df, key_selector='topos'):
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


def parse_topos_place_refs(data='topos_text_data/'):
    directory = os.fsencode(data)
    topos_places = {}
    print("Parsing data...please be patient.")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # print(filename)
        if filename.endswith(".htm") or filename.endswith(".html"):
            # print("here!")
            name = "topos_text_data/" + filename
            text = open(name, "r", encoding="utf8").read()
            soup = BeautifulSoup(text, 'html.parser')
            title = soup.find('meta', property='dc:title', itemprop='name', lang='en').get_text("|")
            elements = title.split("|")
            for element in elements:
                if len(element) > 1:
                    short_title = element
                    # print(short_title)
                    break
            topos_places[short_title] = []
            place_refs = soup.find_all('a', {"class": "place"})
            for ref in place_refs:
                link = ref['about'].split("/")[-1]
                topos_places[short_title].append(link)
        else:
            continue
    print("Parsed " + str(len(topos_places)) + " documents.")
    return topos_places


def merge_pleiades_topos_ids(topos_places):
    df = load_json(topos_gaz)
    ids = topos_pleiades_ids(df)
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