"""This module represents a Pleiades location.

Notes
-----
"Locations in Pleiades connect places to coordinates in space. A location identifies a specific area of interest on
the earth’s surface that is associated with a place during a particular date range. A place can contain multiple
locations. Locations, on the other hand, are associated with one and only one place. Depending on the state of the
evidence, the association between location and place may vary in certainty; some places, attested by name in ancient
sources, may have no associated location at all because modern scholarship cannot pinpoint reliably the ancient site
or area in question."

Notes from https://pleiades.stoa.org/help/conceptual-overview.
"""


class Location:
    """Represents a Pleiades location.

    Parameters
    ----------
    location_data : dictionary
        Section of JSON file relevant to Location objects, parsed as dictionary


    Attributes
    ----------
    geometric_type
    coordinates
    time_periods
    confidence_metrics
    attestations
    location_id
    location_feature_type_uri
    start_date
    end_date
    title
    archaeological_remains
    location_details
    location_accuracy_value
    location_accuracy_info
    location_feature_type
    location_description
    location_type
    location_uri

    Methods
    -------
    print_attestations()
        Print formatted list of temporal attestations
    print_time_periods_info()
        Print information about time periods
    print_confidence_metrics_info()
        Print information about confidence metrics
    report(detail='short')
        Print a summary of information about this location
    """

    def __init__(self, location_data):
        self._time_periods = {}
        self._confidence_metrics = {}
        self._attestations = []
        self._location_id = None
        self._location_feature_type = None
        self._location_feature_type_uri = None
        self._start_date = None
        self._end_date = None
        self._title = None
        self._archaeologicalRemains = None
        self._location_details = None
        self._accuracy_info = None
        self._location_accuracy_value = None
        self._location_featureType = None
        self._location_description = None
        self._location_locationType = None
        self._location_uri = None
        self._geometric_type = None
        self._location_coordinates = []

        if location_data['attestations']:
            for attestation in range(len(location_data['attestations'])):
                time_period = location_data['attestations'][attestation]['timePeriod']
                time_period_uri = location_data['attestations'][attestation]['timePeriodURI']
                confidence = location_data['attestations'][attestation]['confidence']
                confidence_uri = location_data['attestations'][attestation]['confidenceURI']
                if time_period not in self._time_periods.keys():
                    self._time_periods[time_period] = time_period_uri
                if confidence not in self.confidence_metrics.keys():
                    self._confidence_metrics[confidence] = confidence_uri
                self._attestations.append([time_period, confidence])
        if location_data['id']:
            self._location_id = location_data['id']
        if location_data['featureTypeURI'] and location_data['featureTypeURI'][0]:
            self._location_feature_type = location_data['featureType'][0]
            self._location_feature_type_uri = location_data['featureTypeURI'][0]
        if location_data['start']:
            self._start_date = location_data['start']
        if location_data['end']:
            self._end_date = location_data['end']
        if location_data['title']:
            self._title = location_data['title']
        if location_data['archaeologicalRemains']:
            self._archaeologicalRemains = location_data['archaeologicalRemains']
        if location_data['details']:
            self._location_details = location_data['details']
        if location_data['accuracy_value']:
            self._location_accuracy_value = location_data['accuracy_value']
        if location_data['accuracy']:
            self._accuracy_info = location_data['accuracy']
        if location_data['description']:
            self._location_description = location_data['description']
        if location_data['locationType'] and location_data['locationType'][0]:
            self._location_locationType = location_data['locationType'][0]
        if location_data['uri']:
            self._location_uri = location_data['uri']
        if location_data['geometry'] and location_data['geometry']['type']:
            self._geometric_type = location_data['geometry']['type']
        if location_data['geometry'] and location_data['geometry']['coordinates']:
            if len(location_data['geometry']['coordinates']) > 1:  # only one set of coordinates
                self._location_coordinates.append(location_data['geometry']['coordinates'])
            elif len(location_data['geometry']['coordinates'][0]) > 1:
                for coordinate in location_data['geometry']['coordinates'][0]:
                    self._location_coordinates.append(coordinate)
            else:
                for coordinate in location_data['geometry']['coordinates'][0][0]:
                    self._location_coordinates.append(coordinate)

    @property
    def geometric_type(self):
        """Spatial geometry of a particular location (`string`)"""
        return self._geometric_type

    @property
    def coordinates(self):
        """List of geographic coordinates relevant to a location (`list`)"""
        return self._location_coordinates

    @property
    def time_periods(self):
        """Time periods and associated informational uris (`dictionary`)"""
        return self._time_periods

    @property
    def confidence_metrics(self):
        """Confidence metrics and associated informational uris (`dictionary`)"""
        return self._confidence_metrics

    @property
    def attestations(self):
        """Temporal attestations and associated confidence values for a location (`dictionary`)"""
        return self._attestations

    @property
    def location_id(self):
        """Unique identifier for this location (`string`)"""
        return self._location_id

    @property
    def location_feature_type_uri(self):
        """Info link for deprecated attribute (`string`)"""
        return self._location_feature_type_uri

    @property
    def start_date(self):
        """The minimum date (decimal CE year) of any attested time period (`int`)"""
        return self._start_date

    @property
    def end_date(self):
        """The maximum date (decimal CE year) of any attested time period (`int`)"""
        return self._end_date

    @property
    def title(self):
        """Title of location (`string`)"""
        if self._title is None:
            return self._location_id
        return self._title

    @property
    def archaeological_remains(self):
        """Attribute indicating whether archaeological remains are known to be visible at a particular location and,
        if so, how substantive they are (`string`)
        """
        return self._archaeologicalRemains

    @property
    def location_details(self):
        """English-language text providing discussion of a location above and beyond that included in the
        “description (`string`)”
        """
        return self._location_details

    @property
    def location_accuracy_value(self):
        """Pleiades provided accuracy value for a location (`float`)"""
        return self._location_accuracy_value

    @property
    def location_accuracy_info(self):
        """URL for information about provided accuracy value (`string`)"""
        return self._accuracy_info

    @property
    def location_feature_type(self):
        """Deprecated attribute (`string`)"""
        return self._location_featureType

    @property
    def location_description(self):
        """Text description of this location (`string`)"""
        return self._location_description

    @property
    def location_type(self):
        """Location category within Pleiades database (`string`)
        Limited to 'associated modern,' 'central point', 'legacy,' 'representative,' and 'relocated modern.'
        """
        return self._location_locationType

    @property
    def location_uri(self):
        """Pleiades URI for this location (`string`)"""
        return self._location_uri

    def print_attestations(self):
        """Print formatted list of temporal attestations."""
        print("Temporal attestations for " + self.title + ":")
        for attestation in self.attestations:
            print(attestation[0] + ", " + attestation[1])

    def print_time_periods_info(self):
        """Print information about time periods."""
        print("Time periods relevant to " + self.title + ":")
        for time_period in self.time_periods.keys():
            print("--- " + str(time_period) + " ---")
            print(self.time_periods[time_period])

    def print_confidence_metrics_info(self):
        """Print information about confidence metrics."""
        print("Confidence metrics relevant to " + self.title + ":")
        for metric in self.confidence_metrics.keys():
            print("--- " + str(metric) + " ---")
            print(self.confidence_metrics[metric])

    def report(self, detail='short'):
        """Print a summary of information about this location.

        Parameters
        ----------
        detail : {'short', 'long'}
            about of detail to include in summary
        """
        print("Title: " + str(self.title))
        print("ID: " + str(self.location_id))
        print("URI: " + str(self.location_uri))
        print("Date range: " + str(self.start_date) + " - " + str(self.end_date))
        print("Description: " + str(self.location_description))
        if detail == 'long':
            print("Details: " + str(self.location_details))
            # print("Feature type: " + str(self.location_feature_type))
            print("Archaeological remains: " + str(self.archaeological_remains))
            print("Accuracy value: " + str(self.location_accuracy_value))
        print("Location type: " + str(self.location_type))
        print("Temporal attestations: ")
        for att in self.attestations:
            print("    " + str(att[0]) + ", " + str(att[1]))
        if detail == 'long':
            print("Geometric type: " + str(self.geometric_type))
            print("Coordinates: ")
            for coord in self.coordinates:
                print("     " + str(coord))
