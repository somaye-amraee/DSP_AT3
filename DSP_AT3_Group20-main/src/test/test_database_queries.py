import os
import sys
import unittest
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.database.queries import *

class TestGetTablesListQuery(unittest.TestCase):
    """
    Class used for testing get_tables_list_query() from src/database/queries.py
    """
    
    def test_get_tables_list_query(self):
        expected_query = "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema not in ('information_schema', 'pg_catalog')"
        actual_query = get_tables_list_query()
        self.assertEqual(expected_query, actual_query)

class TestGetTableDataQuery(unittest.TestCase):
    """
    Class used for testing get_table_data_query() from src/database/queries.py
    """

    def test_get_table_data_query(self):
        schema_name = 'public'
        table_name = 'user'
        expected_query = f'SELECT * FROM {schema_name}.{table_name}'
        actual_query = get_table_data_query(schema_name, table_name)
        self.assertEqual(expected_query, actual_query)

class TestGetTableSchemaQuery(unittest.TestCase):
    """
    Class used for testing get_table_schema_query() from src/database/queries.py
    """

    def test_get_table_schema_query(self):
        schema_name = 'public'
        table_name = 'user'
        expected_query = f"SELECT * FROM information_schema.columns WHERE table_schema = '{schema_name}' and table_name = '{table_name}'"
        actual_query = get_table_schema_query(schema_name, table_name)
        self.assertEqual(expected_query, actual_query)

if __name__ == '__main__':
    unittest.main(verbosity=2)