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
        how precise of a geographic location.py this is
    formal_title : string
        formal title of location.py
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
        list of Name objects, contains info about attested names for this location.py

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
        Numeric id of the location.py
    subjects : list
        List of subjects relevant to the location.py
    title : string
        Standardized text title
    details : string
        Details about the location.py
    uri: string
        Stable Pleiades uri for the location.py
    description : string
        Long description of location.py
    place_types : list
        List of place types relevant to the location.py
    min_longitude : string
        Minimum longitude of a location.py
    min_latitude : string
        Minimum latitude of a location.py
    max_longitude : string
        Maximum longitude of a location.py
    max_latitude : string
        Maximum latitude of a location.py
    representative_point : list
        Representative long/lat point

    association_certainty_types : dictionary
        maps association certainty values to stable explanatory link
    time_periods : dictionary
        maps time periods to stable explanatory link
    confidence_metrics : dictionary
        maps confidence metrics to stable explanatory link
    location_types : dictionary
        maps location.py types to stable explanatory link

    Information about the other attributes in the object may be found in the Pleiades documentation:
    https://pleiades.stoa.org/downloads
    '''
    def __init__(self, data):
        # initialization
        self._locations = {}
        self._time_periods = {}
        self._confidence_metrics = {}
        self._attestations = []
        self._names = {}
        self._geographic_coordinates = []
        self._location_types = {}
        self._connections = {}
        self._subjects = []
        self._place_types = []
        self._association_certainty_types = {}
        self._geographic_type = None
        self._features_id = None
        self._snippet = None
        self._stable_Pleiades_link = None
        self._description = None
        self._location_precision = None
        self._formal_title = None
        self._id = None
        self._uri = None
        self._description = None
        self._title = None
        self._provenance = None
        self._details = None
        self._type = None
        self._min_longitude = None
        self._min_latitude = None
        self._max_longitude = None
        self._max_latitude = None
        self._representative_point = None

        if data['features'] and data['features'][0]:
            if data['features'][0]['geometry']:
                self._geographic_type = data['features'][0]['geometry']['type']
                for item in data['features'][0]['geometry']['coordinates']:
                    self._geographic_coordinates.append(item)
            if data['features'][0]['id']:
                self._features_id = data['features'][0]['id']
            if data['features'][0]['properties']:
                self._snippet = data['features'][0]['properties']['snippet']
                self._stable_Pleiades_link = data['features'][0]['properties']['link']
                self._description = data['features'][0]['properties']['description']
                self._location_precision = data['features'][0]['properties']['location_precision']
                self._formal_title = data['features'][0]['properties']['title']

        # location.py info
        if data['locations'] and data['locations'][0]:
            if type(data['locations'][0]) == 'dict':  # more than one associated location.py
                for l in data['locations']:
                    current = Location(data['locations'][l])
                    if data['locations'][l]['associationCertainty']:
                        if data['locations'][l]['associationCertainty'] not in self._association_certainty_types.keys():
                            self._association_certainty_types[data['locations'][l]['associationCertainty']] = data['locations'][0]['associationCertaintyURI']
                        self._locations[current] = data['locations'][l]['associationCertainty']
                    else:
                        self._locations[current] = "None"
                    if data['locations'][l]['featureTypeURI'] and data['locations'][l]['featureTypeURI'][0]:
                        location_type = data['locations'][l]['featureType'][0]
                        location_type_uri = data['locations'][l]['featureTypeURI'][0]
                        if location_type not in self._location_types.keys():
                            self._location_types[location_type] = location_type_uri
            else:
                current = Location(data['locations'][0])
                if data['locations'][0]['associationCertainty']:
                    if data['locations'][0]['associationCertainty'] not in self._association_certainty_types.keys():
                        self._association_certainty_types[data['locations'][0]['associationCertainty']] = \
                            data['locations'][0]['associationCertaintyURI']
                    self._locations[current] = data['locations'][0]['associationCertainty']
                else:
                    self._locations[current] = "None"
                if data['locations'][0]['featureTypeURI'] and data['locations'][0]['featureTypeURI'][0]:
                    location_type = data['locations'][0]['featureType'][0]
                    location_type_uri = data['locations'][0]['featureTypeURI'][0]
                    if location_type not in self._location_types.keys():
                        self._location_types[location_type] = location_type_uri
        # connections
        if data['connections'] and data['connections'][0]:
            for item in data['connections']:
                self._connections[item['id']] = item['connectionType']

        # general
        if data['names'] and data['names'][0]:
            if type(data['names'][0]) == 'dict':  # more than one associated name
                for n in data['names']:
                    current = Name(data['names'][n])
                    if data['names'][n]['associationCertainty']:
                        if data['names'][n]['associationCertainty'] not in self._association_certainty_types.keys():
                            self._association_certainty_types[data['names'][n]['associationCertainty']] = data['names'][0]['associationCertaintyURI']
                        self._names[current] = data['names'][n]['associationCertainty']
                    else:
                        self._locations[current] = "None"
            #### HERE::::
            else:
                current = Location(data['locations'][0])
                if data['locations'][0]['associationCertainty']:
                    if data['locations'][0]['associationCertainty'] not in self._association_certainty_types.keys():
                        self._association_certainty_types[data['locations'][0]['associationCertainty']] = \
                            data['locations'][0]['associationCertaintyURI']
                    self._locations[current] = data['locations'][0]['associationCertainty']
                else:
                    self._locations[current] = "None"
                if data['locations'][0]['featureTypeURI'] and data['locations'][0]['featureTypeURI'][0]:
                    location_type = data['locations'][0]['featureType'][0]
                    location_type_uri = data['locations'][0]['featureTypeURI'][0]
                    if location_type not in self._location_types.keys():
                        self._location_types[location_type] = location_type_uri
            list_of_names = data['names']
            for name in range(len(list_of_names)):
                self._names.append(Name(list_of_names[name]))
        #need to make names a dictionary with association certainities, like location

        if data['id']:
            self._id = data['id']
        if data['subject'] and data['subject'][0]:
            for subject in data['subject']:
                self._subjects.append(subject)
        if data['title']:
            self._title = data['title']
        if data['provenance']:
            self._provenance = data['provenance']
        if data['details']:
            self._details = data['details']
        if data['type']:
            self._type = data['type']
        if data['uri']:
            self._uri = data['uri']
        if data['description']:
            self._description = data['description']

        if data['placeTypes'] and data['placeTypes'][0]:
            for place_type in data['placeTypes']:
                self._place_types.append(place_type)

        if data['bbox'] and data['bbox'][0]:
            self._min_longitude = data['bbox'][0]
            self._min_latitude = data['bbox'][1]
            self._max_longitude = data['bbox'][2]
            self._max_latitude = data['bbox'][3]

        if data['reprPoint'] and data['reprPoint'][0]:
            self._representative_point = data['reprPoint']

    # Properties #

    @property
    def locations(self):
        return self._locations

    @property
    def time_periods_info(self):
        return self._time_periods

    @property
    def confidence_metrics_info(self):
        return self._confidence_metrics

    @property
    def attestations(self):
        return self._attestations

    @property
    def names(self):
        return self._names

    @property
    def geographic_coordinates(self):
        return self._geographic_coordinates

    @property
    def location_types_info(self):
        return self._location_types

    @property
    def connections(self):
        return self._connections

    @property
    def subjects(self):
        return self._subjects

    @property
    def place_types(self):
        return self._place_types

    @property
    def association_certainty_info(self):
        return self._association_certainty_types

    @property
    def geographic_type(self):
        return self._geographic_type

    @property
    def features_id(self):
        return self._features_id

    @property
    def snippet(self):
        return self._snippet

    @property
    def pleiades_link(self):
        return self._stable_Pleiades_link

    @property
    def description(self):
        return self._description

    @property
    def location_precision(self):
        return self._location_precision

    @property
    def title(self):
        if self._formal_title is None:
            return self._id
        return self._formal_title

    @property
    def provenance(self):
        return self._provenance

    @property
    def details(self):
        return self._details

    @property
    def type(self):
        return self._type

    @property
    def min_longitude(self):
        return self._min_longitude

    @property
    def min_latitude(self):
        return self._min_latitude

    @property
    def max_longitude(self):
        return self._max_longitude

    @property
    def max_latitude(self):
        return self._max_latitude

    @property
    def representative_point(self):
        return self._representative_point

    # access methods #
    def get_bbox(self):
        return [self.min_latitude, self.min_longitude, self.max_latitude, self.max_longitude]

    def earliest_date(self):
        earliest = 3000
        for location in self.locations.keys():
            if location.start_date < earliest:
                earliest = location.start_date
        return earliest

    def latest_date(self):
        latest = -10000
        for location in self.locations.keys():
            if location.end_date > latest:
                latest = location.end_date
        return latest

    def get_location_ids(self):
        location_ids = []
        for location in self.locations.keys():
            location_ids.append(location.location_id)
        return location_ids

    def get_name_ids(self):
        name_ids = []
        for name in self.names:
            name_ids.append(name.name_id)
        return name_ids

    # Print Methods #

    def __str__(self):
        p = self.title + " (" + self.snippet + ")"
        return p

    def print_time_periods_info(self):
        print("Time periods relevant to " + self.title + ":")
        for time_period in self.time_periods_info.keys():
            print("--- " + str(time_period) + " ---")
            print (self.time_periods_info[time_period])

    def print_confidence_metrics_info(self):
        print("Confidence metrics relevant to " + self.title + ":")
        for metric in self.confidence_metrics_info.keys():
            print("--- " + str(metric) + " ---")
            print (self.confidence_metrics_info[metric])

    def print_location_types_info(self):
        print("Location types relevant to " + self.title + ":")
        for location_type in self.location_types_info.keys():
            print("--- " + str(location_type) + " ---")
            print (self.location_types_info[location_type])

    def print_association_certainty_info(self):
        print("Explanation of association certainties relevent to " + self.title + ":")
        for certainty_type in self.association_certainty_info.keys():
            print("--- " + str(certainty_type) + " ---")
            print(self.association_certainty_info[certainty_type])

    def print_coordinate_info(self):
        print("Set of relevant geographic coordinates (Shape: " + str(self.geographic_type) + "): ")
        if len(self.geographic_coordinates) > 1:
            print("Geographic coordinates: " + "(" + str(self.geographic_coordinates[0]) + ", " + str(
                self.geographic_coordinates[1]) + ")")
        elif len(self.geographic_coordinates[0]) > 1:
            print("Geographic coordinates: ")
            for coord in self.geographic_coordinates[0]:
                print("(" + str(coord[0]) + ", " + str(coord[1]) + ")")
        else:
            print("Geographic coordinates: ")
            for coord in self.geographic_coordinates[0][0]:
                print("(" + str(coord[0]) + ", " + str(coord[1]) + ")")
        print("Representative point: " + str(self.representative_point))
        print("Minimum latitude: " + str(self.min_latitude))
        print("Minimum longitude: " + str(self.min_longitude))
        print("Maximum latitude: " + str(self.max_latitude))
        print("Maximum longitude: " + str(self.max_longitude))

    def print_locations(self):
        print("Locations relevant to " + self.title + ":")
        for location in self.locations.keys():
            print("     " + str(location.title) + " (" + str(location.start_date) + ", ") + str(location.end_date) + ")"

    def print_location_association_certainties(self):
        print("Locations and association certainties relevant to " + self.title + ":")
        for location in self.locations.keys():
            print("     " + location.title + ", " + str(self.locations[location]))

    def print_subjects(self):
        pr = "Subjects relevant to : " + self.title + ": "
        for subject in self.subjects:
            pr = pr + subject + ", "
        print(pr[:-2])

    # Needs to be revised
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







