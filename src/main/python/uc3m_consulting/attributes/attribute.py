import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class Attribute:
    """Base class for validated attributes"""

    def __init__(self, value):
        self._validation_pattern = None
        self._error_message = "Invalid attribute"
        self._attr_value = None

    def validate(self, value):
        """Validate the received value using the configured pattern"""
        if self._validation_pattern is None:
            raise EnterpriseManagementException("Validation pattern not defined")

        if not re.fullmatch(self._validation_pattern, str(value)):
            raise EnterpriseManagementException(self._error_message)

        return value

    @property
    def value(self):
        """Return the validated value"""
        return self._attr_value
