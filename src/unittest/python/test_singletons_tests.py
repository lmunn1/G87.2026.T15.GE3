"""Test file to test the Singleton Pattern on different modules"""
from unittest import TestCase
from uc3m_consulting import EnterpriseManager
from uc3m_consulting.storage import ProjectsJsonStore, DocumentsJsonStore, NumDocsJsonStore

# One test for each singleton class
class SingletonTest(TestCase):
    """Class for testing singletons"""
    def test_enterprise_manager_singleton(self):
        enterprise_manager1 = EnterpriseManager()
        enterprise_manager2 = EnterpriseManager()
        enterprise_manager3 = EnterpriseManager()
        self.assertEqual(enterprise_manager1, enterprise_manager2)
        self.assertEqual(enterprise_manager1, enterprise_manager3)
        self.assertEqual(enterprise_manager2, enterprise_manager3)

    def test_projects_json_store_singleton(self):
        first_instance = ProjectsJsonStore()
        second_instance = ProjectsJsonStore()
        third_instance = ProjectsJsonStore()
        self.assertEqual(first_instance, second_instance)
        self.assertEqual(first_instance, third_instance)
        self.assertEqual(second_instance, third_instance)

    def test_documents_json_store_singleton(self):
        first_instance = DocumentsJsonStore()
        second_instance = DocumentsJsonStore()
        third_instance = DocumentsJsonStore()
        self.assertEqual(first_instance, second_instance)
        self.assertEqual(first_instance, third_instance)
        self.assertEqual(second_instance, third_instance)

    def test_num_docs_json_store_singleton(self):
        first_instance = NumDocsJsonStore()
        second_instance = NumDocsJsonStore()
        third_instance = NumDocsJsonStore()
        self.assertEqual(first_instance, second_instance)
        self.assertEqual(first_instance, third_instance)
        self.assertEqual(second_instance, third_instance)
