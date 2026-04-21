"""Enterprise Manager module for project registration and document queries"""
import re
import json

from datetime import datetime, timezone
from freezegun import freeze_time
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE,
                                                       TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.project_document import ProjectDocument

class EnterpriseManager:
    """Service class for registering projects and querying project documents"""
    def __init__(self):
        pass

    # Code Duplication: This helper handles date logic for validate_starting_date and find_docs.
    @staticmethod
    def _parse_date(date_value: str):
        """Validate a date string and return the parsed date"""
        date_pattern = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        match = date_pattern.fullmatch(date_value)
        if not match:
            raise EnterpriseManagementException("Invalid date format")
        try:
            return datetime.strptime(date_value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

    # Code Duplication: This helper handles JSON file loading logic
    @staticmethod
    def _load_json_file(file_path, default_on_missing=None):
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

    # Code Duplication: This helper handles JSON writing logic
    @staticmethod
    def _write_json_file(file_path, data):
        """Write JSON data to a file."""
        try:
            with open(file_path, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex

    @staticmethod
    def validate_cif(cif_code: str):
        """Validates a cif number"""
        if not isinstance(cif_code, str):
            raise EnterpriseManagementException("CIF code must be a string")
        cif_pattern = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not cif_pattern.fullmatch(cif_code):
            raise EnterpriseManagementException("Invalid CIF format")

        cif_prefix = cif_code[0]
        cif_digits = cif_code[1:8]
        cif_control_char = cif_code[8]

        even_position_sum = 0
        odd_position_sum = 0

        for index in range(len(cif_digits)):
            if index % 2 == 0:
                doubled_digit = int(cif_digits[index]) * 2
                if doubled_digit > 9:
                    even_position_sum = even_position_sum + (doubled_digit // 10) + (doubled_digit % 10)
                else:
                    even_position_sum = even_position_sum + doubled_digit
            else:
                odd_position_sum = odd_position_sum + int(cif_digits[index])

        total_sum = even_position_sum + odd_position_sum
        units_digit = total_sum % 10
        expected_control_digit = 10 - units_digit

        if expected_control_digit == 10:
            expected_control_digit = 0

        control_letters = "JABCDEFGHI"

        if cif_prefix in ('A', 'B', 'E', 'H'):
            if str(expected_control_digit) != cif_control_char:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif cif_prefix in ('P', 'Q', 'S', 'K'):
            if control_letters[expected_control_digit] != cif_control_char:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")
        return True

    def validate_starting_date(self, starting_date):
        """validates the  date format  using regex"""
        parsed_date = self._parse_date(starting_date)

        if parsed_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if parsed_date.year < 2025 or parsed_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")
        return starting_date

    #pylint: disable=too-many-arguments, too-many-positional-arguments
    def register_project(self,
                         company_cif: str,
                         project_acronym: str,
                         project_description: str,
                         department: str,
                         date: str,
                         budget: str):
        """registers a new project"""
        self.validate_cif(company_cif)
        acronym_pattern = re.compile(r"^[a-zA-Z0-9]{5,10}")
        match = acronym_pattern.fullmatch(project_acronym)
        if not match:
            raise EnterpriseManagementException("Invalid acronym")
        description_pattern = re.compile(r"^.{10,30}$")
        match = description_pattern.fullmatch(project_description)
        if not match:
            raise EnterpriseManagementException("Invalid description format")

        department_pattern = re.compile(r"(HR|FINANCE|LEGAL|LOGISTICS)")
        match = department_pattern.fullmatch(department)
        if not match:
            raise EnterpriseManagementException("Invalid department")

        self.validate_starting_date(date)

        try:
            parsed_budget  = float(budget)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        budget_text = str(parsed_budget)
        if '.' in budget_text:
            decimal_places = len(budget_text.split('.')[1])
            if decimal_places > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if parsed_budget < 50000 or parsed_budget > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")


        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=project_acronym,
                                        project_description=project_description,
                                        department=department,
                                        starting_date=date,
                                        project_budget=budget)

        stored_projects = self._load_json_file(PROJECTS_STORE_FILE, default_on_missing=[])

        for stored_project in stored_projects:
            if stored_project == new_project.to_json():
                raise EnterpriseManagementException("Duplicated project in projects list")

        stored_projects.append(new_project.to_json())

        self._write_json_file(PROJECTS_STORE_FILE, stored_projects)

        return new_project.project_id


    def find_docs(self, date_str):
        """
        Generates a JSON report counting valid documents for a specific date.

        Checks cryptographic hashes and timestamps to ensure historical data integrity.
        Saves the output to 'resultado.json'.

        Args:
            date_str (str): date to query.

        Returns:
            number of documents found if report is successfully generated and saved.

        Raises:
            EnterpriseManagementException: On invalid date, file IO errors,
                missing data, or cryptographic integrity failure.
        """
        self._parse_date(date_str)

        # open documents
        stored_documents = self._load_json_file(TEST_DOCUMENTS_STORE_FILE)

        document_count = 0

        # loop to find
        for document_record in stored_documents:
            register_timestamp = document_record["register_date"]

            # string conversion for easy match
            doc_date_str = datetime.fromtimestamp(register_timestamp).strftime("%d/%m/%Y")

            if doc_date_str == date_str:
                document_datetime = datetime.fromtimestamp(register_timestamp, tz=timezone.utc)
                with freeze_time(document_datetime):
                    # check the project id (thanks to freezetime)
                    # if project_id are different then the data has been
                    #manipulated
                    project_document = ProjectDocument(document_record["project_id"], document_record["file_name"])
                    if project_document.document_signature == document_record["document_signature"]:
                        document_count = document_count + 1
                    else:
                        raise EnterpriseManagementException("Inconsistent document signature")

        if document_count == 0:
            raise EnterpriseManagementException("No documents found")
        # prepare json text
        report_timestamp = datetime.now(timezone.utc).timestamp()
        report_entry = {"Querydate":  date_str,
             "ReportDate": report_timestamp,
             "Numfiles": document_count
             }

        stored_reports = self._load_json_file(TEST_NUMDOCS_STORE_FILE, default_on_missing=[])

        stored_reports.append(report_entry)

        self._write_json_file(TEST_NUMDOCS_STORE_FILE, stored_reports)

        return document_count
