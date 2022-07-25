""" This module represents a Name object.
A place may have more than one name.

Notes
-----

References
----------

"""

class Name:
    """
    A class to represent a  name.

    Attributes
    ----------
    name_type
    transcription_accuracy
    description
    name_uri
    romanized_name
    name_id
    transcription_completeness
    language
    name_attestations

    association_certainty : string
        level of certainty in association between place or names





    name_attested : string
        Attested spelling of ancient name, not necessarily the same as the "title"

    Methods
    -------


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
        """type of place the name refers to, e.g. geographic (`string`)"""
        return self._name_type

    @property
    def name_attestations(self):
        """dictionary of temporal attestations of this name;
        maps time periods to confidence metrics (`dictionary`)
        """
        return self._name_attestations

    @property
    def transcription_accuracy(self):
        """accuracy of name as transmitted (`string`)"""
        return self._transcription_accuracy

    @property
    def association_certainty(self):
        return self._association_certainty

    @property
    def romanized_name(self):
        """transliteration of the attested name to Roman characters (`string`)"""
        return self._romanized_name

    @property
    def transcription_completeness(self):
        """how complete the transcribed place name is (`string`)"""
        return self._transcription_completeness

    @property
    def name_id(self):
        """unique identifier for this name (`string`)"""
        return self._name_id

    @property
    def language(self):
        """Short identifier for language and writing system associated with the
        attested spelling (`string`)
        """
        return self._language

    @property
    def description(self):
        """description of name and source (`string`)"""
        return self._description

    @property
    def name_uri(self):
        """uri of the name on Pleiades (`string`)"""
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