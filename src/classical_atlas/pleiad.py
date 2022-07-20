'''
Class header

'''

from name import Name
from location import Location


class Pleiad:
    '''
    A class to represent a single place from Pleiades.

    ---Attributes---
    geographic_type : string
    geographic_coordinates : list
    features_type : string
    features_id : string

    snippet : string
        short description of a place
    link : string
        stable link to Pleiades page
    description : string
        description of a place
    location_precision : string
        how precise of a geographic location this is
    formal_title : string
        formal title of location
    association_certainty : string
        certainty of the relationship between place name and coordinates
    attestations : list
        list of tuples containing temporal attestations and associated confidence metrics
    locations_id : string
    start_date : string
        The minimum date (decimal CE year) of any attested time period.
    end_date : string
        The maximum date (decimal CE year) of any attested time period.
    archaeological_remains : string
        How many archaeological remains are present at the site
    connections : dictionary
        connections to other Pleiades
    names : list
        list of Name objects, contains info about attested names for this location

    locations_details : string
    locations_accuracy_value : string
    locations_featureType : string
    locations_description : string
    locations_locationType : string
    locations_uri : string
    locations_type : string

    type : string
    provenance : string

    id : string
        Numeric id of the location
    subjects : list
        List of subjects relevant to the location
    title : string
        Standardized text title
    details : string
        Details about the location
    uri: string
        Stable Pleiades uri for the location
    description : string
        Long description of location
    place_types : list
        List of place types relevant to the location
    min_longitude : string
        Minimum longitude of a location
    min_latitude : string
        Minimum latitude of a location
    max_longitude : string
        Maximum longitude of a location
    max_latitude : string
        Maximum latitude of a location
    representative_point : list
        Representative long/lat point

    association_certainty_types : dictionary
        maps association certainty values to stable explanatory link
    time_periods : dictionary
        maps time periods to stable explanatory link
    confidence_metrics : dictionary
        maps confidence metrics to stable explanatory link
    location_types : dictionary
        maps location types to stable explanatory link

    Information about the other attributes in the object may be found in the Pleiades documentation:
    https://pleiades.stoa.org/downloads
    '''
    def __init__(self, data):
        # initialization
        self.locations = {}
        self.time_periods = {}
        self.confidence_metrics = {}
        self.attestations = []
        self.names = []
        self.geographic_coordinates = []
        self.location_types = {}
        self.connections = {}
        self.subjects = []
        self.place_types = []
        self.association_certainty_types = {}
        self.connections = {}
        self.geographic_type = None
        self.features_id = None
        self.snippet = None
        self.stable_Pleiades_link = None
        self.description = None
        self.location_precision = None
        self.formal_title = None

        if data['features'] and data['features'][0]:
            if data['features'][0]['geometry']:
                self.geographic_type = data['features'][0]['geometry']['type']
                for item in data['features'][0]['geometry']['coordinates']:
                    self.geographic_coordinates.append(item)
            if data['features'][0]['id']:
                self.features_id = data['features'][0]['id']
            if data['features'][0]['properties']:
                self.snippet = data['features'][0]['properties']['snippet']
                self.stable_Pleiades_link = data['features'][0]['properties']['link']
                self.description = data['features'][0]['properties']['description']
                self.location_precision = data['features'][0]['properties']['location_precision']
                self.formal_title = data['features'][0]['properties']['title']

        # location info
        if data['locations'] and data['locations'][0]:
            if type(data['locations'][0]) == 'dict':  # more than one associated location
                for l in data['locations']:
                    current = Location(data['locations'][l])
                    if data['locations'][l]['associationCertainty']:
                        if data['locations'][l]['associationCertainty'] not in self.association_certainty_types.keys():
                            self.association_certainty_types[data['locations'][l]['associationCertainty']] = data['locations'][0]['associationCertaintyURI']
                        self.locations[current] = data['locations'][l]['associationCertainty']
                    else:
                        self.locations[current] = "None"
                    if data['locations'][l]['featureTypeURI'] and data['locations'][l]['featureTypeURI'][0]:
                        location_type = data['locations'][l]['featureType'][0]
                        location_type_uri = data['locations'][l]['featureTypeURI'][0]
                        if location_type not in self.location_types.keys():
                            self.location_types[location_type] = location_type_uri
            else:
                current = Location(data['locations'][0])
                if data['locations'][0]['associationCertainty']:
                    if data['locations'][0]['associationCertainty'] not in self.association_certainty_types.keys():
                        self.association_certainty_types[data['locations'][0]['associationCertainty']] = \
                            data['locations'][0]['associationCertaintyURI']
                    self.locations[current] = data['locations'][0]['associationCertainty']
                else:
                    self.locations[current] = "None"
                if data['locations'][0]['featureTypeURI'] and data['locations'][0]['featureTypeURI'][0]:
                    location_type = data['locations'][0]['featureType'][0]
                    location_type_uri = data['locations'][0]['featureTypeURI'][0]
                    if location_type not in self.location_types.keys():
                        self.location_types[location_type] = location_type_uri
        # connections
        if data['connections'] and data['connections'][0]:
            for item in data['connections']:
                self.connections[item['id']] = item['connectionType']

        # general
        if data['names'] and data['names'][0]:
            list_of_names = data['names']
            for name in range(len(list_of_names)):
                self.names.append(Name(list_of_names[name]))

        self.id = None
        self.uri = None
        self.description = None
        self.title = None
        self.provenance = None
        self.details = None
        self.type = None
        self.min_longitude = None
        self.min_latitude = None
        self.max_longitude = None
        self.max_latitude = None
        self.representative_point = None
        if data['id']:
            self.id = data['id']
        if data['subject'] and data['subject'][0]:
            for subject in data['subject']:
                self.subjects.append(subject)
        if data['title']:
            self.title = data['title']
        if data['provenance']:
            self.provenance = data['provenance']
        if data['details']:
            self.details = data['details']
        if data['type']:
            self.type = data['type']
        if data['uri']:
            self.uri = data['uri']
        if data['description']:
            self.description = data['description']

        if data['placeTypes'] and data['placeTypes'][0]:
            for place_type in data['placeTypes']:
                self.place_types.append(place_type)

        if data['bbox'] and data['bbox'][0]:
            self.min_longitude = data['bbox'][0]
            self.min_latitude = data['bbox'][1]
            self.max_longitude = data['bbox'][2]
            self.max_latitude = data['bbox'][3]

        if data['reprPoint'] and data['reprPoint'][0]:
            self.representative_point = data['reprPoint']

    def __str__(self):
        p = self.title + " (" + self.snippet + ")"
        return p

    def full_report(self):
        print("Geographic type: " + str(self.geographic_type))
        if len(self.geographic_coordinates) > 1:
            print("Geographic coordinates: " + "(" + str(self.geographic_coordinates[0]) + ", " + str(self.geographic_coordinates[1])+ ")")
        elif len(self.geographic_coordinates[0]) > 1:
            print("Geographic coordinates: ")
            for coord in self.geographic_coordinates[0]:
                print("(" + str(coord[0]) + ", " + str(coord[1]) + ")")
        else:
            print("Geographic coordinates: ")
            for coord in self.geographic_coordinates[0][0]:
                print("(" + str(coord[0]) + ", " + str(coord[1]) + ")")
        print("Features id: " + str(self.features_id))
        print("Snippet: " + str(self.snippet))
        print("Stable Pleiades link: " + str(self.stable_Pleiades_link))
        print("Description: " + str(self.description))
        print("Location precision: " + str(self.location_precision))
        print("Formal title: " + str(self.formal_title))
        print("Locations: ")
        for location in self.locations.keys():
            print(" - " + str(location.title) + ", " + str(location.start_date) + "-" + str(location.end_date) + ", " + str(self.locations[location]))
        print("Connections: ")
        for item in self.connections.keys():
            print(" - " + item + ": " + str(self.connections[item]))
        print("Names: ")
        for item in self.names:
            print(" - " + str(item))
        print("ID : " + self.id)
        print("Subjects: ")
        for item in self.subjects:
            print(" - " + str(item))
        print("Title : " + str(self.title))
        print("Provenance : " + str(self.provenance))
        print("Details : " + str(self.details))
        print("Type : " + str(self.type))
        print("uri : " + str(self.uri))
        print("Description : " + str(self.description))
        print("Place types: ")
        for item in self.place_types:
            print(" - " + str(item))
        print("Minimum longitude : " + str(self.min_longitude))
        print("Minimum latitude : " + str(self.min_latitude))
        print("Maximum longitude : " + str(self.max_longitude))
        print("Maximum latitude : " + str(self.max_latitude))
        print("Representative point : " + str(self.representative_point))







