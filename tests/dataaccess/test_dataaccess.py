from unittest import TestCase
from ti.dataaccess.utils import *


class TestDataaccess(TestCase):

    def test_basic_json_datastore_creation(self):
        datastore = get_data_store("JSON")
        self.assertIsNotNone(datastore, 'Should not be none, but is')

    def test_loading_json_datastore(self):
        datastore = get_data_store("JSON")
        data = datastore.load()
        self.assertIsNotNone(data, 'Should not be none, but is')
        self.assertIsNotNone(data['work'], 'Data should have empty work list, but doesn\'t')
