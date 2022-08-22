"""
Classical Atlas
module header
@author: kalamar

"""
from collections import defaultdict
import networkx as nx
import downloaders
from pleiad import Pleiad
import topos_wrangler


def make_pleiades_objects(download_latest_data=False):
    if download_latest_data:
        print("Warning: Pleiades data files are large and may require considerable time to download.")
        input("Press Enter to continue...")
        data = downloaders.get_pleiades_data(
            "http://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz")
    else:
        raw_data_file = downloaders.unzip_gz("data/pleiades-places-latest.json.gz")
        data = downloaders.get_df(raw_data_file)
    data = data['@graph']
    pleiades = []
    for row in range(len(data)):
        pleiades.append(Pleiad(data[row]))
    return pleiades


def find_keyword(list_of_pleiads, keyword, print_results=False):
    """Search through text fields of pleiad objects, locations, and names for a specified keyword.

    Parameters
    ----------
    list_of_pleiads : list
        list of pleiad objects to search through
    keyword : string
        keyword to search for
    print_results : boolean, default=False
        if True, print results before returning

    Returns
    -------
    dictionary
        dictionary of lists; contains pleiad objects, locations, and names relavant to keyword
    """
    found_list = defaultdict(list)
    for pleiad in list_of_pleiads:
        if (pleiad.description and keyword in pleiad.description) \
                or (pleiad.details and keyword in pleiad.details) \
                or (pleiad.title and keyword in pleiad.title):
            found_list['pleiad'].append(pleiad)
        for location in pleiad.locations.keys():
            if (location.title and keyword in location.title) \
                    or (location.location_description and keyword in location.location_description) \
                    or (location.location_details and keyword in location.location_details):
                found_list['location'].append(location)
        for name in pleiad.names.keys():
            if keyword in name.romanized_name \
                    or (name.description and keyword in name.description) \
                    or (name.language and keyword in name.language):
                found_list['name'].append(name)
    if print_results:
        print("Pleiades relevant to keyword " + keyword + ": ")
        for pl in found_list['pleiad']:
            print("     " + pl.title)
        print("Locations relevant to keyword " + keyword + ": ")
        for loc in found_list['location']:
            print("     " + loc.title)
        print("Names relevant to keyword " + keyword + ": ")
        for name in found_list['name']:
            print("     " + name.romanized_name)
    return found_list


def get_pleiades_as_nodes(list_of_pleiades):
    """
    Add nodes representing places to a graph.

    Parameters
    ----------
    list_of_pleiades : list
        a list of Pleiades objects

    Returns
    -------
    Graph
        a NetworkX Graph with nodes representing places
    """
    G = nx.Graph()
    for pl in list_of_pleiades:
        G.add_node(pl)
    return G


def add_connections_as_edges(graph):
    """
    Adds edges between places with connections.

    Parameters
    ----------
    graph : Graph
        a networkX Graph with defined nodes

    Returns
    -------
    Graph
        a networkX Graph with added edges
    """
    temp = []
    for node in graph.nodes:
        temp.append(node)
    for pl in temp:
        for connection in pl.connections.keys():
            match = None
            for node in temp:
                if connection == node.id:
                    match = node
                    break
            graph.add_edge(pl, match, connection_type=pl.connections[connection][0])
    return graph


def get_pleiades_network_shortcut():
    """
    Get a network of representing the entire Pleiades dataset.

    Returns
    -------
    graph
        a NetworkX graph with nodes representing Pleiades places and edges representing connections between places
    """
    pleiades = make_pleiades_objects()
    gr = get_pleiades_as_nodes(pleiades)
    gr = add_connections_as_edges(gr)
    return gr


def add_topos_text_data_to_network(graph):
    """
    Add topos text data to the network.

    Parameters
    ----------
    graph : Graph
        a graph with nodes representing Pleiades objects

    Returns
    -------
    Graph
        a Graph with added node attributes of list of textual references
    """
    df = topos_wrangler.get_topos_data()
    topos_refs = topos_wrangler.switch_to_pleiades_ids(df, topos_wrangler.parse_topos_place_refs())
    topos_refs = topos_wrangler.swap_key_value_pairs(topos_refs)
    G = nx.Graph()
    for topos_id in topos_refs.keys():
        for node in graph.nodes:
            if node.id == topos_id:
                G.add_node(node, textual_refs=topos_refs[topos_id])
