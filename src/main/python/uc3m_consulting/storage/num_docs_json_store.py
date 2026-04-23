"""Module for logic relating to num docs JSON"""
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE
from uc3m_consulting.storage.json_store import JsonStore


class NumDocsJsonStore:
    """Num docs json store class"""
    class __NumDocsJsonStore:
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
            stored_reports = NumDocsJsonStore().load_reports()
            stored_reports.append(report_entry)
            NumDocsJsonStore().save_reports(stored_reports)

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = cls.__NumDocsJsonStore()
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
