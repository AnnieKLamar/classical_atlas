"""
Classical Atlas : A Python Package for Open-Access Geospatial Datasets about the Ancient World
Developed by Annie K. Lamar (Stanford University | kalamar@stanford.edu)

This module contains the methods you will use most often. With these methods, you can parse all Pleiades data,
create Pleiad objects representing Pleiades Places, add Places to a networkX graph, add edges representing
connections between places, and even add node attributes from other datasets (e.g. ToposText) to the graph.

To quickly obtain a graph all Pleiades places and connections, use the method **get_pleiades_network_shortcut.** You
can also use the methods individually if you want to change the default settings. To add data from ToposText,
create a graph of Pleiad objects and use **add_topos_text_data_to_network()**, passing the graph as a parameter.
"""
from collections import defaultdict
import networkx as nx
import downloaders
from pleiad import Pleiad
import topos_wrangler


def make_pleiades_objects(download_latest_data=False):
    """
    Parses Pleiades data and returns a list of Pleiad objects. Each Pleiad object represents a single Pleiades place.
    With default settings, this method will use the JSON file included in the release of this Python package. If you
    want to make sure you are using the most recent Pleiades JSON file, set the parameter **download_latest_data=True**.
    Note that downloading recent data will take quite a while.
    """
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
    """Search through text fields of Pleiad objects, locations, and names for a specified keyword.

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
    Add nodes representing places to a graph. Each node is a Pleiades "Place" and has linked Locations and Names.

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
    Adds edges between places with connections. These connections are taken from the Pleiades metadata. Connection
    type is also included as an edge attribute. More information about connections is available here:
    https://pleiades.stoa.org/help/what-are-connections.

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
    Get a networkX Graph representing the entire Pleiades dataset. This method is a shortcut to parse all Pleiades
    data, create Pleiad objects representing every Pleiades place with linked Locations and Names, add those objects
    to a Graph as nodes, and add edges that represent connections (and their attributes) between Places. This method
    takes no arguments and returns a networkX Graph object.

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
    Add topos text data to the network. This method parses through all Topos Text data, matches the Topos Text data
    to Pleiades IDs when possible, and adds a list of textual references as a node attribute. The graph that you pass
    to this method should be a networkX Graph object created with the methods found in the pleiades_wrangler module.
    Edges are not required, but do not impact the functionality if present. The returned Graph is the same except
    nodes have one added attribute: a list of texts that reference that particular place.

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
    return G
