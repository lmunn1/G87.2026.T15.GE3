from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE
from uc3m_consulting.storage.json_store import JsonStore


class ProjectsJsonStore:
    """Storage class for project persistence"""

    @staticmethod
    def load_projects():
        """Load and return stored projects"""
        return JsonStore.load_json_file(PROJECTS_STORE_FILE, default_on_missing=[])

    @staticmethod
    def save_projects(projects):
        """Save the full list of projects"""
        JsonStore.write_json_file(PROJECTS_STORE_FILE, projects)

    @staticmethod
    def check_project_not_duplicated(stored_projects, new_project):
        """Check project is not already stored."""
        for stored_project in stored_projects:
            if stored_project == new_project.to_json():
                raise EnterpriseManagementException(
                    "Duplicated project in projects list"
                )

    @staticmethod
    def add_project(new_project):
        """Add a new project to storage."""
        stored_projects = ProjectsJsonStore.load_projects()
        ProjectsJsonStore.check_project_not_duplicated(
            stored_projects,
            new_project
        )
        stored_projects.append(new_project.to_json())
        ProjectsJsonStore.save_projects(stored_projects)