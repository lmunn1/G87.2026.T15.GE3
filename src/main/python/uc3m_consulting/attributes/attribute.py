import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class Attribute:
    """Base class for validated attributes"""

    def __init__(self, attr_value, validation_pattern, error_message):
        self._validation_pattern = validation_pattern
        self._error_message = error_message
        self._attr_value = self.validate(attr_value)

    def validate(self, value):
        """Validate the received value using the configured pattern"""
        if not re.fullmatch(self._validation_pattern, str(value)):
            raise EnterpriseManagementException(self._error_message)
        return value

    @property
    def value(self):
        """Return the validated value"""
        return self._attr_value
