"""Enterprise Manager module for project registration and document queries"""
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_manager_config import (TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.document_manager import DocumentManager
from uc3m_consulting.storage import JsonStore, ProjectsJsonStore, DocumentsJsonStore
from uc3m_consulting.attributes import (
    ProjectAcronym, ProjectDepartment,
    ProjectDescription, DateAttribute,
    ProjectDateAttribute, CifAttribute,
    ProjectBudgetAttribute
)
class EnterpriseManager:
    """Service class for registering projects and querying project documents"""
    class __EnterpriseManager:
        """Service class for registering projects and querying project documents"""
        def __init__(self):
            pass

        #pylint: disable=too-many-arguments, too-many-positional-arguments
        @staticmethod
        def register_project(company_cif: str,
                             project_acronym: str,
                             project_description: str,
                             department: str,
                             date: str,
                             budget: str):
            """registers a new project"""
            validated_cif = CifAttribute(company_cif)

            validated_acronym = ProjectAcronym(project_acronym)

            validated_description = ProjectDescription(project_description)

            validated_department = ProjectDepartment(department)

            validated_date = ProjectDateAttribute(date)

            validated_budget = ProjectBudgetAttribute(budget)

            new_project = EnterpriseProject(company_cif=validated_cif.value,
                                            project_acronym=validated_acronym.value,
                                            project_description=validated_description.value,
                                            department=validated_department.value,
                                            starting_date=validated_date.value,
                                            project_budget=validated_budget.value)


            ProjectsJsonStore().add_project(new_project)

            return new_project.project_id

        @staticmethod
        def find_docs(date_str):
            """Find docs method to locate the documents and return the count"""
            DateAttribute(date_str)

            stored_documents = DocumentsJsonStore.load_documents()

            document_count = 0

            for document_record in stored_documents:
                if DocumentManager.document_matches_date(document_record, date_str):
                    DocumentManager.check_document_signature(document_record)
                    document_count = document_count + 1

            DocumentManager.check_documents_found(document_count)

            report_entry = DocumentManager.build_report_entry(date_str, document_count)

            stored_reports = JsonStore.load_json_file(
                TEST_NUMDOCS_STORE_FILE,
                default_on_missing=[]
            )

            stored_reports.append(report_entry)

            JsonStore.write_json_file(TEST_NUMDOCS_STORE_FILE, stored_reports)

            return document_count

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = cls.__EnterpriseManager()
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
