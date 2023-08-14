import unittest
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.dataframe.queries import *

class TestGetqueries(unittest.TestCase):
    def setUp(self):
        self.schema_name = 'public'
        self.table_name = 'test'
    
    def test_get_numeric(self):
        result = get_numeric_tables_query(self.schema_name, self.table_name)
        expect = f"select column_name from information_schema.columns as col where col.data_type in ('smallint', 'integer', 'bigint','decimal', 'numeric', 'real', 'double precision','smallserial', 'serial', 'bigserial', 'money') and col.table_schema not in ('information_schema', 'pg_catalog') and col.table_schema = '{self.schema_name}' and col.table_name = '{self.table_name}'"
        
        self.assertEqual(result, expect)
    def test_get_text(self):
        result = get_text_tables_query(self.schema_name, self.table_name)
        expect = f"select column_name from information_schema.columns as col where col.data_type in ('char', 'varchar', 'text') and col.table_schema not in ('information_schema', 'pg_catalog') and col.table_schema = '{self.schema_name}' and col.table_name = '{self.table_name}'"

        self.assertEqual(result, expect)

    def test_get_date(self):
        result = get_date_tables_query(self.schema_name, self.table_name)
        expect = f"select column_name from information_schema.columns as col where col.data_type in ('date', 'time', 'timestamp', 'timestampz', 'timetz') and col.table_schema not in ('information_schema', 'pg_catalog') and col.table_schema = '{self.schema_name}' and col.table_name = '{self.table_name}'"
        
        self.assertEqual(result, expect)

    def test_get_primary(self):
        result = get_primary_key(self.schema_name, self.table_name)
        expect = f"select c.column_name from information_schema.table_constraints t left join information_schema.constraint_column_usage c on c.constraint_name = t.constraint_name where t.table_schema = '{self.schema_name}' and t.constraint_type = 'PRIMARY KEY' and t.table_name = '{self.table_name}'"

        self.assertEqual(result, expect)

if __name__ == '__main__':
    unittest.main(verbosity=2)