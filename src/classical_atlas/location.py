class Location:

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
        self._location_accuracy_value = None
        self._location_featureType = None
        self._location_description = None
        self._location_locationType = None
        self._location_uri = None

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
        if location_data['description']:
            self._location_description = location_data['description']
        if location_data['locationType'] and location_data['locationType'][0]:
            self._location_locationType = location_data['locationType'][0]
        if location_data['uri']:
            self._location_uri = location_data['uri']

    @property
    def time_periods(self):
        return self._time_periods

    @property
    def confidence_metrics(self):
        return self._confidence_metrics

    @property
    def attestations(self):
        return self._attestations

    @property
    def location_id(self):
        return self._location_id

    @property
    def location_feature_type_uri(self):
        return self._location_feature_type_uri

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def title(self):
        if self._title is None:
            return self._location_id
        return self._title

    @property
    def archaeological_remains(self):
        return self._archaeologicalRemains

    @property
    def location_details(self):
        return self._location_details

    @property
    def location_accuracy_value(self):
        return self._location_accuracy_value

    @property
    def location_feature_type(self):
        return self._location_featureType

    @property
    def location_description(self):
        return self._location_description

    @property
    def location_type(self):
        return self._location_locationType

    @property
    def location_uri(self):
        return self._location_uri

    def print_attestations(self):
        print("Temporal attestations for " + self.title + ":")
        for attestation in self.attestations:
            print(attestation[0] + ", " + attestation[1])
