from datetime import datetime, timezone

from uc3m_consulting.attributes.date_attribute import DateAttribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class ProjectDateAttribute(DateAttribute):
    """Definition of project date attribute class"""

    def __init__(self, attr_value):
        super().__init__(attr_value)

        parsed_date = datetime.strptime(self.value, "%d/%m/%Y").date()

        if parsed_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException(
                "Project's date must be today or later."
            )

        if parsed_date.year < 2025 or parsed_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")