from datetime import datetime, timezone

from freezegun import freeze_time

from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.project_document import ProjectDocument


class DocumentManager:
    """Helper class for document query and report logic"""

    @staticmethod
    def document_matches_date(document_record, date_str):
        """Return True if the document register date matches the query date"""
        register_timestamp = document_record["register_date"]
        doc_date_str = datetime.fromtimestamp(register_timestamp).strftime("%d/%m/%Y")
        return doc_date_str == date_str

    @staticmethod
    def check_document_signature(document_record):
        """Check whether the stored document signature is consistent"""
        register_timestamp = document_record["register_date"]
        document_datetime = datetime.fromtimestamp(register_timestamp, tz=timezone.utc)

        with freeze_time(document_datetime):
            project_document = ProjectDocument(
                document_record["project_id"],
                document_record["file_name"]
            )

            if project_document.document_signature != document_record["document_signature"]:
                raise EnterpriseManagementException("Inconsistent document signature")

    @staticmethod
    def build_report_entry(date_str, document_count):
        """Build the report entry for the queried date."""
        report_timestamp = datetime.now(timezone.utc).timestamp()
        return {
            "Querydate": date_str,
            "ReportDate": report_timestamp,
            "Numfiles": document_count
        }

    @staticmethod
    def check_documents_found(document_count):
        """Raise exception if no matching documents were found."""
        if document_count == 0:
            raise EnterpriseManagementException("No documents found")