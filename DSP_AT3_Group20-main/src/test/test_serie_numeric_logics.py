import unittest
import pandas as pd
import datetime
from unittest import mock
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.serie_numeric.logics import NumericColumn
from src.database.logics import PostgresConnector



@mock.patch('src.database.logics.PostgresConnector')
class TestInstantiation(unittest.TestCase):    
    def test_instantiation(self, mock_db):
        schema_name = 'public'
        table_name = 'orders'
        col_name = 'order_id'
        db = mock_db
        serie = mock_db.load_table(schema_name, table_name)[col_name]

        numeric_serie = NumericColumn(schema_name, table_name, col_name, db, serie)
        self.assertEqual(numeric_serie.schema_name, schema_name)
        self.assertEqual(numeric_serie.table_name, table_name)
        self.assertEqual(numeric_serie.db, db)
        self.assertEqual(numeric_serie.serie, serie)

@mock.patch('src.serie_numeric.logics.NumericColumn.is_serie_none')
class TestIsdfnone(unittest.TestCase):
    def test_empty(self, mock_none):
        mock_none.return_value = 'The serie is empty'
        serie = NumericColumn(None, None, None, None, None)
        result = serie.is_serie_none()
        expect = 'The serie is empty'
        self.assertEqual(result, expect)

    def test_several_null(self, mock_none):
        cnt_null = 2
        mock_none.return_value = f'The serie has {cnt_null} null.'
        serie = NumericColumn(None, None, None, None, None)
        result = serie.is_serie_none()
        expect = 'The serie has 2 null.'
        self.assertEqual(result,expect)
        
    def test_no_null(self, mock_none):
        mock_none.return_value = False
        serie = NumericColumn(None, None, None, None, None)
        result = serie.is_serie_none()
        self.assertFalse(result)

@mock.patch('scr.database.logics.PostgresConnector.run_query')
class TestSetunique(unittest.TestCase):
    def setUp(self):
        self.serie = NumericColumn(None, None, None, None, None)
        self.serie.db = PostgresConnector(None, None, None, None, None)
    def test_set_unique(self, mock_unique):
        mock_unique.return_value = pd.DataFrame([4], columns=['count'])
        self.serie.set_unique()
        result= self.serie.n_unique
        expect = 4 
        self.assertEqual(result,expect)



class TestSetmissing(unittest.TestCase):
    def setUp(self):
        self.serie = NumericColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([None, None, None, None, 1], name= 'test')
    def test_set_missing(self):
        self.serie.set_missing()
        result = self.serie.n_missing
        expect = 4
        self.assertEqual(result, expect)

class TestSetmean(unittest.TestCase):
    def setUp(self):
        self.serie = NumericColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([1,2,3,8,5,5,4,6], name= 'test')
    def test_set_mean(self):    
        self.serie.set_mean()
        result = self.serie.col_mean
        expect = 4.25
        self.assertEqual(result, expect)



class TestSetmin(unittest.TestCase):
    def setUp(self):
        self.serie = NumericColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([1,2,3,4,5,5,7,5], name= 'test')
    def test_set_min(self):    
        self.serie.set_min()
        result = self.serie.col_min
        expect = 1
        self.assertEqual(result, expect)

class TestSetmax(unittest.TestCase):
    def setUp(self):
        self.serie = NumericColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([1,2,3,4,5,5,7,5], name= 'test')
    def test_set_max(self):    
        self.serie.set_max()
        result = self.serie.col_max
        expect = 7
        self.assertEqual(result, expect)


        
class TestSetmedian(unittest.TestCase):
    def setUp(self):
        self.serie = NumericColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([1,2,3,4,5,5,6,6], name= 'test')
    def test_set_median(self):    
        self.serie.set_median()
        result = self.serie.col_median
        expect = 4.5
        self.assertEqual(result, expect)


                    


        