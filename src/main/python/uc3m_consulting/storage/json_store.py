import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class JsonStore:
    # Code Duplication: Added helper
    @staticmethod
    def load_json_file(file_path, default_on_missing=None):
        """Load and return JSON data from a file."""
        try:
            with open(file_path, "r", encoding="utf-8", newline="") as file:
                return json.load(file)
        except FileNotFoundError as ex:
            if default_on_missing is not None:
                return default_on_missing
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex

    # Code Duplication: Added helper
    @staticmethod
    def write_json_file(file_path, data):
        """Write JSON data to a file."""
        try:
            with open(file_path, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex