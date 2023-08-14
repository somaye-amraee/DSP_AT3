import unittest
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.serie_numeric.queries import *

class Tsetqueries(unittest.TestCase):
    def test_get_negative_number_query(self):
        result = get_negative_number_query('test', 'test','test')
        expect = "select count(test) as negative_number from test.test where test<0"

        self.assertEqual(result, expect)

    def test_get_std_query(self):
        result = get_std_query('test', 'test', 'test')
        expect = "select STDDEV(test) from test.test"
        
        self.assertEqual(result, expect)

    def test_get_unique_queryt(self):
        result = get_unique_query('test', 'test','test')
        expect = "select count(distinct(test)) from test.test"

        self.assertEqual(result, expect)

if __name__ == '__main__':
    unittest.main(verbosity=2)