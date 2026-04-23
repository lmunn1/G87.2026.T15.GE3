from uc3m_consulting.attributes.attribute import Attribute

class ProjectDescription(Attribute):
    """Definition of attribute description class"""

    def __init__(self, attr_value):
        super().__init__(
            attr_value,
            r"^.{10,30}$",
            "Invalid description format"
        )

