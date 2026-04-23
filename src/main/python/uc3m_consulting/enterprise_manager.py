"""Enterprise Manager module for project registration and document queries"""
import re

from datetime import datetime, timezone
from freezegun import freeze_time

from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE,
                                                       TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.storage import JsonStore, ProjectsJsonStore
from uc3m_consulting.attributes import ProjectAcronym, ProjectDepartment, ProjectDescription, DateAttribute

class EnterpriseManager:
    """Service class for registering projects and querying project documents"""
    def __init__(self):
        pass

    # Long Functions: Added helper
    @staticmethod
    def _calculate_cif_control_digit(cif_digits: str):
        """Calculate the expected control digit for a CIF."""
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

    # Long Functions: Added helper
    @staticmethod
    def _validate_budget(budget: str):
        """Validate budget and return parsed float"""
        try:
            parsed_budget = float(budget)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        budget_text = str(parsed_budget)
        if '.' in budget_text:
            decimal_places = len(budget_text.split('.')[1])
            if decimal_places > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if parsed_budget < 50000 or parsed_budget > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")

        return parsed_budget

    # Long Functions: Added helper
    @staticmethod
    def _check_project_not_duplicated(stored_projects, new_project):
        """Check project is not already stored"""
        for stored_project in stored_projects:
            if stored_project == new_project.to_json():
                raise EnterpriseManagementException("Duplicated project in projects list")

    # Long Functions: Added helper
    @staticmethod
    def _document_matches_date(document_record, date_str):
        """Return True if the document register date matches the query date."""
        register_timestamp = document_record["register_date"]
        doc_date_str = datetime.fromtimestamp(register_timestamp).strftime("%d/%m/%Y")
        return doc_date_str == date_str

    # Long Functions: Added helper
    @staticmethod
    def _check_document_signature(document_record):
        """Check whether the stored document signature is consistent."""
        register_timestamp = document_record["register_date"]
        document_datetime = datetime.fromtimestamp(register_timestamp, tz=timezone.utc)

        with freeze_time(document_datetime):
            project_document = ProjectDocument(
                document_record["project_id"],
                document_record["file_name"]
            )

            if project_document.document_signature != document_record["document_signature"]:
                raise EnterpriseManagementException("Inconsistent document signature")

    # Long Functions: Added helper
    @staticmethod
    def _build_report_entry(date_str, document_count):
        """Build the report entry for the queried date."""
        report_timestamp = datetime.now(timezone.utc).timestamp()
        return {
            "Querydate": date_str,
            "ReportDate": report_timestamp,
            "Numfiles": document_count
        }

    # Long Functions: Added helper
    @staticmethod
    def _check_documents_found(document_count):
        """Raise exception if no matching documents were found."""
        if document_count == 0:
            raise EnterpriseManagementException("No documents found")

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
        expected_control_digit = EnterpriseManager._calculate_cif_control_digit(cif_digits)

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
        """Validates the  date format  using regex"""
        validated_date = DateAttribute(starting_date)
        parsed_date = datetime.strptime(validated_date.value, "%d/%m/%Y").date()

        if parsed_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if parsed_date.year < 2025 or parsed_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")

        return validated_date

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

        validated_acronym = ProjectAcronym(project_acronym)

        validated_description = ProjectDescription(project_description)

        validated_department = ProjectDepartment(department)

        validated_date = self.validate_starting_date(date)

        self._validate_budget(budget)

        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=validated_acronym.value,
                                        project_description=validated_description.value,
                                        department=validated_department.value,
                                        starting_date=validated_date.value,
                                        project_budget=budget)

        ProjectsJsonStore.add_project(new_project)

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
        DateAttribute(date_str)

        # open documents
        stored_documents = JsonStore.load_json_file(TEST_DOCUMENTS_STORE_FILE)

        document_count = 0

        # loop to find
        for document_record in stored_documents:
            if self._document_matches_date(document_record, date_str):
                self._check_document_signature(document_record)
                document_count = document_count + 1

        self._check_documents_found(document_count)

        # prepare json text
        report_entry = self._build_report_entry(date_str, document_count)

        stored_reports = JsonStore.load_json_file(TEST_NUMDOCS_STORE_FILE, default_on_missing=[])

        stored_reports.append(report_entry)

        JsonStore.write_json_file(TEST_NUMDOCS_STORE_FILE, stored_reports)

        return document_count
