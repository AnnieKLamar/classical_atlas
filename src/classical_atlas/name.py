class Name:
    """
    A class to represent a location.py name.

    ---Attributes---
    name_type : string
        name of the location.py
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
        self._name_type = None
        self._transcription_accuracy = None
        self._association_certainty = None
        self._romanized_name = None
        self._name_attestations = {}
        self._name_id = None
        self._transcription_completeness = None
        self._language = None
        self._description = None
        self._name_uri = None
        self._name_attested = None

        if attributes['nameType']:
            self._name_type = attributes['nameType']
        if attributes['transcriptionAccuracy']:
            self._transcription_accuracy = attributes['transcriptionAccuracy']
        if attributes['associationCertainty']:
            self._association_certainty = attributes['associationCertainty']
        if attributes['romanized']:
            self._romanized_name = attributes['romanized']
        if attributes['attestations']:
            list_of_attestations = attributes['attestations']
            for attestations in list_of_attestations:
                self._name_attestations[attestations['timePeriod']] = attestations['confidence']
        if attributes['id']:
            self._name_id = attributes['id']
        if attributes['transcriptionCompleteness']:
            self._transcription_completeness = attributes['transcriptionCompleteness']
        if attributes['language']:
            self._language = attributes['language']
        if attributes['description']:
            self._description = attributes['description']
        if attributes['uri']:
            self._name_uri = attributes['uri']
        if attributes['attested']:
            self._name_attested = attributes['attested']

    @property
    def name_type(self):
        return self._name_type

    @property
    def name_attestations(self):
        return self._name_attestations

    @property
    def transcription_accuracy(self):
        return self._transcription_accuracy

    @property
    def association_certainty(self):
        return self._association_certainty

    @property
    def romanized_name(self):
        return self._romanized_name

    @property
    def transcription_completeness(self):
        return self._transcription_completeness

    @property
    def name_id(self):
        return self._name_id

    @property
    def language(self):
        return self._language

    @property
    def description(self):
        return self._description

    @property
    def name_uri(self):
        return self._name_uri

    @property
    def name_attested(self):
        return self._name_attested

    def __str__(self):
        n = "[" + self.name_type + "] " + self.romanized_name
        if self.name_attested is not None:
            n = n + " (" + self.name_attested + ")"
        if self.description is not None:
            n = n + ": " + self.description
        return n

    def name_summary(self):
        print(" ---- Summary of " + self.romanized_name + " (ID: " + str(self.name_id) + ")" + " ----")
        print("Name type: " + str(self.name_type))
        print("Language: " + str(self.language))
        print("Description: " + str(self.description))
        print("Transcription accuracy: " + str(self.transcription_accuracy))
        print("Transcription completeness: " + str(self.transcription_completeness))
        print("Description: " + str(self.description))
        print("Ancient spelling: " + str(self.name_attested))
        if len(self.name_attestations) != 0:
            print("Temporal attestations: ")
            for attestation in self.name_attestations.keys():
                print(" - " + str(attestation) + ", " + str(self.name_attestations[attestation]))