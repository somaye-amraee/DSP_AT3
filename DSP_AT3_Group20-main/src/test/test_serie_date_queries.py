import unittest
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.serie_date.queries import *

class Tsetqueries(unittest.TestCase):
    def test_get_min_date(self):
        result = get_min_date_query('test', 'test','test')
        expect = "select min(test) as min_date from test.test"

        self.assertEqual(result, expect)

    def test_get_weekend_count(self):
        result = get_weekend_count_query('test', 'test', 'test')
        expect = "select count(*) from (select extract(dow from test) as weekend from test.test) as temp where weekend in (0,6)"
        
        self.assertEqual(result, expect)

    def test_get_1900_count(self):
        result = get_1900_count_query('test', 'test','test')
        expect = "select count(*) from (select date(test) as date from test.test) as temp where date = '1900-01-01'"

        self.assertEqual(result, expect)
if __name__ == '__main__':
    unittest.main(verbosity=2)