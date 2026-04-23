"""Module for logic relating to num docs JSON"""
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE
from uc3m_consulting.storage.json_store import JsonStore


class NumDocsJsonStore:
    """Num docs json store class"""

    @staticmethod
    def load_reports():
        """Load and return stored reports"""
        return JsonStore.load_json_file(TEST_NUMDOCS_STORE_FILE, default_on_missing=[])

    @staticmethod
    def save_reports(reports):
        """Save the full list of reports"""
        JsonStore.write_json_file(TEST_NUMDOCS_STORE_FILE, reports)

    @staticmethod
    def add_report(report_entry):
        """Add a new report to storage"""
        stored_reports = NumDocsJsonStore.load_reports()
        stored_reports.append(report_entry)
        NumDocsJsonStore.save_reports(stored_reports)