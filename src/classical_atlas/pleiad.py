"""Module to represent a Pleiades place.

Notes
-----
"Pleiades places are the primary organizational construct of the gazetteer. They are conceptual entities: the term
"place" applies to any locus of human attention, material or intellectual, in a real-world geographic context. A
settlement mentioned in an ancient text is a place, whether or not it can now be located; an archaeological site is a
place; a modern city located atop an ancient settlement is a place. Basically, any spatial feature that is connected
to the pre-modern past and that a human being has noticed and discussed as such between the past and the present is a
place.

Places in Pleiades can therefore represent:

* areas of fairly intensive human activity like settlements and sanctuaries;

* large-scale geological features known in antiquity like mountains, rivers, lakes;

* political, social, or cultural constructs like provinces and mining districts;

* individual structures, when they have been referred to individually by ancient sources or modern scholars (e.g.,
the Parthenon, the Queen’s Megaron at Knossos, the Basilica Iulia, the House of the Faun); and

* Spatial extents or thematic groupings of places defined by modern scholars or administrative entities for purposes of
analysis, description, reference, or heritage management (e.g., the Aswan Quarry Landscape, or the Archaeological
Border complex of Hedeby and the Danevirke) Pleiades recognizes a variety of place categories or types; new
categories can be added as needed by the editorial college.

Places are entirely abstract, conceptual entities. They are objects of thought, speech, or writing, not tangible,
mappable points on the earth’s surface. They have no spatial or temporal attributes of their own. A place can exist
in name only in an ancient source, without any material correlate; conversely, an archaeological site can exist as a
place without an ancient name.

The spatial aspects of Pleiades places (i.e., latitude and longitude coordinates in space), as well as their ancient
and modern names, are addressed through two other conceptual entities: locations and names. Connections are used to
express and document relationships between different places. Temporal characteristics and bibliographical references
are recorded at the name, location, and connection levels as appropriate."

Notes from https://pleiades.stoa.org/help/conceptual-overview.

Note also that this class excludes the deprecated (as of 2010) Pleiades 'features' that are linked to places.
The features container remains in the available Pleiades dataset to preserve spatial metadata.
The intent of the place-location-name distinction makes features containers irrelevant.
"""

from name import Name
from location import Location


class Pleiad:
    """
    A class to represent a single place from Pleiades.

    Attributes
    ----------
    locations
    title
    names
    location_types_info
    connections
    subjects
    place_types
    association_certainty_info
    description
    provenance
    details
    type
    min_longitude
    min_latitude
    max_longitude
    max_latitude
    representative_point
    uri
    id

    Methods
    -------

    Information about the other attributes in the object may be found in the Pleiades documentation:
    https://pleiades.stoa.org/downloads
    """
    def __init__(self, data):
        # initialization
        self._locations = {}
        self._names = {}
        self._location_types = {}
        self._connections = {}
        self._subjects = []
        self._place_types = []
        self._association_certainty_types = {}
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
        # locations
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
                self._connections[item['id']] = [item['connectionType'], item['title'], item['start'], item['end']]
        # names
        if data['names'] and data['names'][0]:
            if type(data['names'][0]) == 'dict':  # more than one associated name
                for n in data['names']:
                    current = Name(data['names'][n])
                    if data['names'][n]['associationCertainty']:
                        if data['names'][n]['associationCertainty'] not in self._association_certainty_types.keys():
                            self._association_certainty_types[data['names'][n]['associationCertainty']] = data['names'][0]['associationCertaintyURI']
                        self._names[current] = data['names'][n]['associationCertainty']
                    else:
                        self._names[current] = "None"
            else:
                current = Name(data['names'][0])
                if data['names'][0]['associationCertainty']:
                    if data['names'][0]['associationCertainty'] not in self._association_certainty_types.keys():
                        self._association_certainty_types[data['names'][0]['associationCertainty']] = \
                            data['names'][0]['associationCertaintyURI']
                    self._names[current] = data['names'][0]['associationCertainty']
                else:
                    self._names[current] = "None"
        # general
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
        """Maps associated locations to certainty of association (`dictionary`)"""
        return self._locations

    @property
    def title(self):
        """Title included in a place's metadata in Pleiades (`string`)"""
        return self._title

    @property
    def names(self):
        """Maps associated names to certainty of association ('dictionary')"""
        return self._names

    @property
    def location_types_info(self):
        """Information about the types of associated locations (`dictionary`)"""
        return self._location_types

    @property
    def connections(self):
        """Information about connections between this place and another (`dictionary`)"""
        return self._connections

    @property
    def subjects(self):
        """List of subjects relevant to this place (`list`)"""
        return self._subjects

    @property
    def place_types(self):
        """Place types associated with a place (`list`)"""
        return self._place_types

    @property
    def association_certainty_info(self):
        """Maps certainty types to corresponding information (`dictionary`)"""
        return self._association_certainty_types

    @property
    def description(self):
        """Text description of a place (`string`)"""
        return self._description

    @property
    def provenance(self):
        """Provenance of information about this place (`string`)"""
        return self._provenance

    @property
    def details(self):
        """Details about a place above and beyond information in the description (`string`)"""
        return self._details

    @property
    def type(self):
        """Deprecated place type variable (`string`)"""
        return self._type

    @property
    def min_longitude(self):
        """Minimum longitude of bounding box (`float`)"""
        return self._min_longitude

    @property
    def min_latitude(self):
        """Minimum latitude of bounding box (`float`)"""
        return self._min_latitude

    @property
    def max_longitude(self):
        """Maximum longitude of bounding box (`float`)"""
        return self._max_longitude

    @property
    def max_latitude(self):
        """Maximum latitude of bounding box (`float`)"""
        return self._max_latitude

    @property
    def representative_point(self):
        """Representative point of latitude and longitude (`list`)"""
        return self._representative_point

    @property
    def uri(self):
        """Stable Pleiades uri for a place (`string`)"""
        return self._uri

    @property
    def id(self):
        """Unique identifier for a place (`string`)"""
        return self._id

    # access methods
    def get_bbox(self):
        """Access bounding box of geographic coordinates

        Returns
        -------
        list
            bounding box of geographic coordinates
        """
        return [self.min_latitude, self.min_longitude, self.max_latitude, self.max_longitude]

    def earliest_date(self):
        """Return earliest known date of any associated location

        Returns
        -------
        int
            Earliest known date of any associated location
        """
        earliest = 3000
        for location in self.locations.keys():
            if location.start_date < earliest:
                earliest = location.start_date
        return earliest

    def latest_date(self):
        """Return latest known date of any associated location

        Returns
        -------
        int
            latest known date of any associated location
        """
        latest = -10000
        for location in self.locations.keys():
            if location.end_date > latest:
                latest = location.end_date
        return latest

    def get_list_of_locations(self):
        """
        Return list of titles of associated locations

        Returns
        -------
        list
            titles of associated locations
        """
        locations = []
        for location in self.locations.keys():
            locations.append(location.title)
        return locations

    def get_location_ids(self):
        """
        Return list of ids of associated locations

        Returns
        -------
        list
            ids of associated locations
        """
        location_ids = []
        for location in self.locations.keys():
            location_ids.append(location.location_id)
        return location_ids

    def get_list_of_names(self):
        """
        Return list of names associated with a place

        Returns
        -------
        list
            names associated with a place
        """
        names_list = []
        for name in self.names.keys():
            names_list.append(name.romanized_name)
        return names_list

    def get_name_ids(self):
        """
        Return list of ids of associated names

        Returns
        -------
        list
            ids of associated names
        """
        name_ids = []
        for name in self.names.keys():
            name_ids.append(name.name_id)
        return name_ids

    # info methods
    def __str__(self):
        p = self.title + " (" + self.description + ")"
        return p

    def print_location_types_info(self):
        """Print explanations for location types."""
        print("Location types relevant to " + self.title + ":")
        for location_type in self.location_types_info.keys():
            print("--- " + str(location_type) + " ---")
            print(self.location_types_info[location_type])

    def print_association_certainty_info(self):
        """Print explanations for association certainties"""
        print("Explanation of association certainties relevant to " + self.title + ":")
        for certainty_type in self.association_certainty_info.keys():
            print("--- " + str(certainty_type) + " ---")
            print(self.association_certainty_info[certainty_type])

    def print_coordinate_info(self):
        """Print information about geographic coordinates associated with a place"""
        print("Representative point: " + str(self.representative_point))
        print("Minimum latitude: " + str(self.min_latitude))
        print("Minimum longitude: " + str(self.min_longitude))
        print("Maximum latitude: " + str(self.max_latitude))
        print("Maximum longitude: " + str(self.max_longitude))

    def print_locations(self):
        """Print summary of titles of locations associated with a place"""
        print("Locations relevant to " + self.title + ":")
        for location in self.locations.keys():
            print("     " + str(location.title) + " (" + str(location.start_date) + ", " + str(location.end_date) + ")")

    def print_location_association_certainties(self):
        """Print summary of locations and association certainties"""
        print("Locations and association certainties relevant to " + self.title + ":")
        for location in self.locations.keys():
            print("     " + location.title + ", " + str(self.locations[location]))

    def print_subjects(self):
        """Print list of relevant subjects"""
        pr = "Subjects relevant to : " + self.title + ": "
        for subject in self.subjects:
            pr = pr + subject + ", "
        print(pr[:-2])

    def print_connections(self):
        """Print list of connections and relevant information"""
        print("Connections relevant to " + self.title + ":")
        for connection in self.connections.keys():
            c_type = self.connections[connection][0]
            c_title = self.connections[connection][1]
            c_start = self.connections[connection][2]
            c_end = self.connections[connection][3]
            print(c_title + " (id: " + str(connection) + "): ")
            print("     connection type: " + str(c_type))
            print("     date range: " + str(c_start) + ", " + str(c_end))

    def report(self, detail='short'):
        """Print a summary of information about this location.

         Parameters
         ----------
         detail : {'short', 'long'}
             about of detail to include in summary
         """
        print("Title : " + str(self.title))
        print("Description : " + str(self.description))
        print("Representative point : " + str(self.representative_point))
        print("ID : " + self.id)
        print("uri : " + str(self.uri))
        print("Place types: ")
        for item in self.place_types:
            print(" - " + str(item))
        if detail == 'long':
            print("Provenance : " + str(self.provenance))
            print("Details : " + str(self.details))
            print("Type : " + str(self.type))
            print("Minimum longitude : " + str(self.min_longitude))
            print("Minimum latitude : " + str(self.min_latitude))
            print("Maximum longitude : " + str(self.max_longitude))
            print("Maximum latitude : " + str(self.max_latitude))
            print("Subjects: ")
            for item in self.subjects:
                print(" - " + str(item))
        print("Locations: ")
        for location in self.locations.keys():
            print(" - " + str(location.title) + ", " + str(location.start_date) + "-" + str(location.end_date) + ", " + str(self.locations[location]))
        print("Connections: ")
        for item in self.connections.keys():
            print(" - " + item + ": " + str(self.connections[item]))
        print("Names: ")
        for item in self.names:
            print(" - " + str(item))

    def place_type_info(self):
        print(self.place_types)
        print("https://pleiades.stoa.org/vocabularies/place-types")
