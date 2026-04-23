import re
from datetime import datetime

from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class DateAttribute(Attribute):
    """Definition of generic date attribute class"""

    def __init__(self, attr_value):
        super().__init__(
            attr_value,
            r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$",
            "Invalid date format"
        )

    def validate(self, value):
        """Validate date format and real calendar date."""
        validated_value = super().validate(value)
        try:
            datetime.strptime(validated_value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex
        return validated_value