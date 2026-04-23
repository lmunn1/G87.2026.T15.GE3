"""Module to perform logic on Projects relating to JSON"""
from uc3m_consulting.enterprise_management_exception import (
    EnterpriseManagementException,
)
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE
from uc3m_consulting.storage.json_store import JsonStore


class ProjectsJsonStore:
    """Storage class for project persistence."""

    class __ProjectsJsonStore:
        """Actual singleton implementation for project storage."""

        @staticmethod
        def load_projects():
            """Load and return stored projects."""
            return JsonStore.load_json_file(
                PROJECTS_STORE_FILE,
                default_on_missing=[]
            )

        @staticmethod
        def save_projects(projects):
            """Save the full list of projects."""
            JsonStore.write_json_file(PROJECTS_STORE_FILE, projects)

        @staticmethod
        def check_project_not_duplicated(stored_projects, new_project):
            """Check project is not already stored."""
            for stored_project in stored_projects:
                if stored_project == new_project.to_json():
                    raise EnterpriseManagementException(
                        "Duplicated project in projects list"
                    )

        def add_project(self, new_project):
            """Add a new project to storage."""
            stored_projects = self.load_projects()
            self.check_project_not_duplicated(
                stored_projects,
                new_project
            )
            stored_projects.append(new_project.to_json())
            self.save_projects(stored_projects)

    instance = None

    def __new__(cls, *args, **kwargs):
        """Return the singleton instance."""
        if cls.instance is None:
            cls.instance = cls.__ProjectsJsonStore()
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
