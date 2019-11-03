import unittest
import json
from unittest.mock import patch
from app import get_doc_owner_name, delete_doc, add_new_doc


documents = []
directories = {}


def setUpModule():
    with open('../fixtures/documents.json', 'r', encoding='utf-8') as data:
        documents.extend(json.load(data))
    with open('../fixtures/directories.json', 'r', encoding='utf-8') as data:
        directories.update(json.load(data))


@patch('app.documents', documents, create=True)
@patch('app.directories', directories, create=True)
class TestSecretaryProgram(unittest.TestCase):

    @patch('app.input', return_value='2207 876234')
    def test_delete_doc(self, input):
        len_start = len(documents)
        delete_doc()
        self.assertGreater(len_start, len(documents))

    @patch('app.input', return_value='10006')
    def test_get_doc_owner_name(self, input):
        foo_return = get_doc_owner_name()
        self.assertIsInstance(foo_return, str)
        self.assertIsNotNone(get_doc_owner_name())

    @patch('app.input', side_effect=['123456', 'doc type', 'Anton', '3'])
    def test_add_new_doc(self, input):
        len_start = len(documents)
        add_new_doc()
        self.assertGreater(len(documents), len_start)


if __name__ == '__main__':
    unittest.main()
