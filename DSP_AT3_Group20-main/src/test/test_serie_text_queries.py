import unittest
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../')) 
from src.serie_text.queries import *

class TestTextQueries(unittest.TestCase):

    def setUp(self):
        self.schema_name = "public"
        self.table_name = "categories"
        self.col_name = "description" 

    def test_get_missing_query(self):
        output = get_missing_query(self.schema_name, self.table_name ,self.col_name)
        expectation = "SELECT COUNT(description) FROM public.categories WHERE 'description' IS NULL"

        self.assertEqual(output, expectation)


    def test_get_mode_query(self):
        output = get_mode_query(self.schema_name, self.table_name ,self.col_name)
        expectation = "SELECT MODE() WITHIN GROUP (ORDER BY description) from public.categories"

        self.assertEqual(output, expectation)


    def test_get_alpha_query(self):
        output = get_alpha_query(self.schema_name, self.table_name ,self.col_name)
        expectation = "select count(description) from public.categories where description ~* '[A-Z]'"

        self.assertEqual(output, expectation)

if __name__ == '__main__':
    unittest.main(verbosity=2)