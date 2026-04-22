from uc3m_consulting.attributes.attribute import Attribute


class ProjectAcronym(Attribute):
    """Definition of attribute acronym class"""

    # pylint: disable=super-init-not-called
    def __init__(self, attr_value):
        self._validation_pattern = r"^[a-zA-Z0-9]{5,10}$"
        self._error_message = "Invalid acronym"
        self._attr_value = self.validate(attr_value)