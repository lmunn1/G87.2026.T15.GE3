"""Handles department validation logic/rules"""
from uc3m_consulting.attributes.attribute import Attribute

class ProjectDepartment(Attribute):
    """Definition of attribute department class"""

    def __init__(self, attr_value):
        super().__init__(
            attr_value,
            r"^(HR|FINANCE|LEGAL|LOGISTICS)$",
            "Invalid department"
        )
