"""Module handling logic related to documents and JSON"""
from uc3m_consulting.enterprise_manager_config import TEST_DOCUMENTS_STORE_FILE
from uc3m_consulting.storage.json_store import JsonStore


class DocumentsJsonStore:
    """Document JSON store class"""
    class __DocumentsJsonStore:
        @staticmethod
        def load_documents():
            """Load and return stored documents"""
            return JsonStore.load_json_file(TEST_DOCUMENTS_STORE_FILE, default_on_missing=[])

        @staticmethod
        def save_documents(documents):
            """Save the full list of documents"""
            JsonStore.write_json_file(TEST_DOCUMENTS_STORE_FILE, documents)

        @staticmethod
        def add_document(new_document):
            """Add a new document to storage"""
            stored_documents = DocumentsJsonStore.load_documents()
            stored_documents.append(new_document.to_json())
            DocumentsJsonStore.save_documents(stored_documents)

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = cls.__DocumentsJsonStore()
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
