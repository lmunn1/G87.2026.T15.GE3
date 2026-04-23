"""Module to handle acronym validation logic"""
from uc3m_consulting.attributes.attribute import Attribute

class ProjectAcronym(Attribute):
    """Definition of attribute acronym class"""

    def __init__(self, attr_value):
        super().__init__(
            attr_value,
            r"^[a-zA-Z0-9]{5,10}$",
            "Invalid acronym"
        )
