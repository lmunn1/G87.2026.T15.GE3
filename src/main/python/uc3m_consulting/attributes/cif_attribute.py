import re

from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class CifAttribute(Attribute):
    """Definition of CIF attribute class"""

    def __init__(self, attr_value):
        super().__init__(attr_value, r"^.*$", "Invalid CIF format")

    @staticmethod
    def _calculate_cif_control_digit(cif_digits: str):
        """Calculate the expected control digit for a CIF"""
        even_position_sum = 0
        odd_position_sum = 0

        for index in range(len(cif_digits)):
            if index % 2 == 0:
                doubled_digit = int(cif_digits[index]) * 2
                if doubled_digit > 9:
                    even_position_sum = (
                        even_position_sum
                        + (doubled_digit // 10)
                        + (doubled_digit % 10)
                    )
                else:
                    even_position_sum = even_position_sum + doubled_digit
            else:
                odd_position_sum = odd_position_sum + int(cif_digits[index])

        total_sum = even_position_sum + odd_position_sum
        units_digit = total_sum % 10
        expected_control_digit = 10 - units_digit

        if expected_control_digit == 10:
            expected_control_digit = 0

        return expected_control_digit

    def validate(self, cif_code: str):
        """Validates a cif number"""
        if not isinstance(cif_code, str):
            raise EnterpriseManagementException("CIF code must be a string")

        cif_pattern = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not cif_pattern.fullmatch(cif_code):
            raise EnterpriseManagementException("Invalid CIF format")

        cif_prefix = cif_code[0]
        cif_digits = cif_code[1:8]
        cif_control_char = cif_code[8]
        expected_control_digit = self._calculate_cif_control_digit(cif_digits)

        control_letters = "JABCDEFGHI"

        if cif_prefix in ('A', 'B', 'E', 'H'):
            if str(expected_control_digit) != cif_control_char:
                raise EnterpriseManagementException(
                    "Invalid CIF character control number"
                )
        elif cif_prefix in ('P', 'Q', 'S', 'K'):
            if control_letters[expected_control_digit] != cif_control_char:
                raise EnterpriseManagementException(
                    "Invalid CIF character control letter"
                )
        else:
            raise EnterpriseManagementException("CIF type not supported")

        return cif_code