"""Module to handle budget validation logic"""
from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class ProjectBudgetAttribute(Attribute):
    """Definition of project budget attribute class"""

    def __init__(self, attr_value):
        super().__init__(attr_value, r"^.*$", "Invalid budget amount")

    def validate(self, budget_value):
        """Validate a project budget"""
        try:
            parsed_budget = float(budget_value)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        decimal_places = 0
        budget_text = str(parsed_budget)
        if "." in budget_text:
            decimal_places = len(budget_text.split(".")[1])
        if decimal_places > 2:
            raise EnterpriseManagementException("Invalid budget amount")

        if parsed_budget < 50000 or parsed_budget > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")

        return parsed_budget
