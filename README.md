---
permalink: docs/index.html
---

# Classical Atlas: A Python Package for Open-Access Geospatial Datasets about the Ancient World
### Developed by Annie K. Lamar (Stanford University | kalamar@stanford.edu)

## Installation

You can install classical_atlas using pip by running the command `pip install classical_atlas`. Classical Atlas requires the following external packages be installed:
- networkx (`pip install networkx`)
- beautifulsoup4 (`pip install beautifulsoup4`)

## Quickstart

The pleiades_wrangler module contains the methods you will use most often. With these methods, you can parse all Pleiades data,
create Pleiad objects representing Pleiades Places, add Places to a networkX graph, add edges representing
connections between places, and even add node attributes from other datasets (e.g. ToposText) to the graph.

To quickly obtain a graph all Pleiades places and connections, use the method `get_pleiades_network_shortcut`. To achieve the same result, you can also run the methods individually, as below:
    
    `list_of_pleiades = make_pleiades_objects`
    `graph_of_nodes_only = get_pleiades_as_nodes(list_of_pleiades)`
    `complete_graph = add_connections_as_edges(graph_of_nodes_only)`

To add data from ToposText, create a graph of Pleiad objects and use `add_topos_text_data_to_network`, passing the graph as a parameter. Here is an example:

`add_topos_text_data_to_network(complete_graph)`

## Object Overview

This package has two types of Python modules: object classes, and wrangler modules. The three object classes are Pleiad, Name, and Location. A Pleiad represents a Pleiades Place, and contains all metadata specific to that Place. Each Pleiad also has attributes of lists of linked locations and names, represented by Location and Names objects.  

Each class has numerous methods for accessing attributes and printing information about a place. For example, you can run `earliest_date()` on a Pleiad object to receive the earliest date associated with any of the linked Location objects. You can also run `report()` on a Pleiad to print a full list of all attributes associated with a particular place. There are many more methods that may be useful. More information about the object attributes and methods is available in the project docs: https://annieklamar.github.io/classical_atlas/ 

The two wrangler modules that exist in the Beta version of this package are `pleiades_wrangler` and `topos_wrangler`. With `pleiades_wrangler`, you can create a graph of Pleiades places as above. You can run a keyword search on a list of Pleiad objects using `find_keyword`. (Note: keyword search through a graph is forthcoming.) With `topos_wrangler`, you can parse all available ToposText data. This module also includes methods to replace ToposText place IDs with Pleiades IDs when available.

## Feedback

This project is in beta. If you can feedback or suggestions, please contact me at kalamar [at] stanford [dot] edu.
