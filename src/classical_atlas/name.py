""" This module represents a Name object.

Notes
-----
Names in Pleiades are also connected with places. A name reflects the
identity of a place in human language, not its physical location in the landscape. Names have no spatial coordinates,
but they are always annotated with the time period(s) of the textual source(s) in which they are attested. As with
locations, a single place can have multiple names, but an individual name can be associated with one and only one
place. This is true even if the same sequence of characters is also attested as a name for another place; Pleiades
treats these “identical” names as separate entities. (https://pleiades.stoa.org/help/conceptual-overview)

"""


class Name:
    """
    A class to represent a  name.

    Parameters
    ----------
    attributes : dictionary
        Section of JSON file relevant to Name objects, parsed as dictionary

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
    name_attested

    Methods
    -------
    name_summary()
        Print summary of Name object
    """

    def __init__(self, attributes):
        self._name_type = None
        self._transcription_accuracy = None
        self._romanized_name = None
        self._name_attestations = {}
        self._name_id = None
        self._transcription_completeness = None
        self._language = None
        self._description = None
        self._name_uri = None
        self._name_attested = None
        self._provenance = None

        if attributes['nameType']:
            self._name_type = attributes['nameType']
        if attributes['transcriptionAccuracy']:
            self._transcription_accuracy = attributes['transcriptionAccuracy']
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
        if attributes['provenance']:
            self._provenance = attributes['provenance']

    @property
    def name_type(self):
        """Type of place the name refers to, e.g. geographic (`string`)"""
        return self._name_type

    @property
    def name_attestations(self):
        """Dictionary of temporal attestations of this name;
        maps time periods to confidence metrics (`dictionary`)
        """
        return self._name_attestations

    @property
    def provenance(self):
        """Provenance of recorded name (`string`)"""
        return self._provenance

    @property
    def transcription_accuracy(self):
        """Accuracy of name as transmitted (`string`)"""
        return self._transcription_accuracy

    @property
    def romanized_name(self):
        """Transliteration of the attested name to Roman characters (`string`)"""
        return self._romanized_name

    @property
    def transcription_completeness(self):
        """How complete the transcribed place name is (`string`)"""
        return self._transcription_completeness

    @property
    def name_id(self):
        """Unique identifier for this name (`string`)"""
        return self._name_id

    @property
    def language(self):
        """Short identifier for language and writing system associated with the
        attested spelling (`string`)
        """
        return self._language

    @property
    def description(self):
        """Description of name and source (`string`)"""
        return self._description

    @property
    def name_uri(self):
        """URI of the name on Pleiades (`string`)"""
        return self._name_uri

    @property
    def name_attested(self):
        """Attested spelling of ancient name, not necessarily the same as the `title` (`string`)"""
        return self._name_attested

    def __str__(self):
        """Represent Name object as a string.

        Returns
        -------
        string
            representation of Name object as string; includes name, temporal attestation, and description
        """
        n = "[" + self.name_type + "] " + self.romanized_name
        if self.name_attested is not None:
            n = n + " (" + self.name_attested + ")"
        if self.description is not None:
            n = n + ": " + self.description
        return n

    def name_summary(self):
        """Print summary of Name object."""
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
