'''


'''




class Pleiad:
    '''
    A class to represent a single location from Pleiades.

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

        if data['features'] and data['features'][0]:
            if data['features'][0]['geometry']:
                self.geographic_type = data['features'][0]['geometry']['type']
                self.geographic_coordinates = data['features'][0]['geometry']['coordinates']
            if data['features'][0]['type']:
                self.features_type = data['features'][0]['type']
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
            if data['locations'][0]['associationCertainty']:
                self.association_certainty = data['locations'][0]['associationCertainty']
                if self.association_certainty not in self.association_certainty_types.keys():
                    self.association_certainty_types[self.association_certainty] = data['locations'][0]['associationCertaintyURI']

            # info about temporal attestations
            if data['locations'][0]['attestations']:
                for attestation in range(len(data['locations'][0]['attestations'])):
                    time_period = data['locations'][0]['attestations'][attestation]['timePeriod']
                    time_period_uri = data['locations'][0]['attestations'][attestation]['timePeriodURI']
                    confidence = data['locations'][0]['attestations'][attestation]['confidence']
                    confidence_uri = data['locations'][0]['attestations'][attestation]['confidenceURI']
                    if time_period not in self.time_periods.keys():
                        self.time_periods[time_period] = time_period_uri
                    if confidence not in self.confidence_metrics.keys():
                        self.confidence_metrics[confidence] = confidence_uri
                    self.attestations.append([time_period, confidence])

            if data['locations'][0]['id']:
                self.locations_id = data['locations'][0]['id']

            if data['locations'][0]['featureTypeURI'] and data['locations'][0]['featureTypeURI'][0]:
                location_type = data['locations'][0]['featureType'][0]
                location_type_uri = data['locations'][0]['featureTypeURI'][0]
                if location_type not in self.location_types.keys():
                    self.location_types[location_type] = location_type_uri

            if data['locations'][0]['start']:
                self.start_date = data['locations'][0]['start']
            if data['locations'][0]['end']:
                self.end_date = data['locations'][0]['end']

            if data['locations'][0]['title']:
                self.locations_title = data['locations'][0]['title']

            if data['locations'][0]['archaeologicalRemains']:
                self.archaeologicalRemains = data['locations'][0]['archaeologicalRemains']
            if data['locations'][0]['details']:
                self.locations_details = data['locations'][0]['details']
            if data['locations'][0]['accuracy_value']:
                self.locations_accuracy_value = data['locations'][0]['accuracy_value']
            if data['locations'][0]['featureType'] and data['locations'][0]['featureType'][0]:
                self.locations_featureType = data['locations'][0]['featureType'][0]
            if data['locations'][0]['description']:
                self.locations_description = data['locations'][0]['description']
            if data['locations'][0]['locationType'] and graph_dict['locations'][0]['locationType'][0]:
                self.locations_locationType = data['locations'][0]['locationType'][0]
            if data['locations'][0]['uri']:
                self.locations_uri = data['locations'][0]['uri']
            if data['locations'][0]['@type']:
                self.locations_type = data['locations'][0]['@type']

        # connections

        if data['connections'] and data['connections'][0]:
            for item in data['connections']:
                self.connections[item['id']] = item['connectionType']

        # general
        if data['names'] and data['names'][0]:
            list_of_names = data['names']
            for name in range(len(list_of_names)):
                self.names.append(Name(list_of_names[name]))

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


class Name:
    """
    A class to represent a location name.

    ---Attributes---
    name_type : string
        name of the location
    transcription_accuracy : string
        accuracy of name as transmitted
    association_certainty : string
        Level of certainty in association between places and locations or names
    romanized_name : string
        Transliteration of the attested name to Roman characters following the
        Classical Atlas Project scheme.
    attestations : AttestationsContainer
        AttestationsContainer object of attestations of this place name
    name_id : string
        id of the name
    transcription_completeness : string
        how complete the transcribed place name is
    language : string
         Short identifier for language and writing system associated with the
         attested spelling
    description : string
        description of name and source
    name_uri : string
        uri of the name on Pleiades
    name_attested : string
        Attested spelling of ancient name, not necessarily the same as the "title"
    """

    def __init__(self, attributes):
        self.name_type = attributes['nameType']
        self.transcription_accuracy = attributes['transcriptionAccuracy']
        self.association_certainty = attributes['associationCertainty']
        self.romanized_name = attributes['romanized']
        self.name_attestations = {}
        list_of_attestations = attributes['attestations']
        for attestations in list_of_attestations:
            self.name_attestations[attestations['timePeriod']] = attestations['confidence']
        self.name_id = attributes['id']
        self.transcription_completeness = attributes['transcriptionCompleteness']
        self.language = attributes['language']
        self.description = attributes['description']
        self.name_uri = attributes['uri']
        self.name_attested = attributes['attested']
