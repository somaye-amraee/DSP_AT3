import datetime
import unittest
import pandas as pd
from unittest import mock
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.serie_date.logics import DateColumn
from src.database.logics import PostgresConnector

@mock.patch('src.database.logics.PostgresConnector')
class TestInstantiation(unittest.TestCase):    
    def test_instantiation(self, mock_db):
        schema_name = 'public'
        table_name = 'orders'
        col_name = 'order_id'
        db = mock_db
        serie = mock_db.load_table(schema_name, table_name)[col_name]

        data_serie = DateColumn(schema_name, table_name, col_name, db, serie)
        self.assertEqual(data_serie.schema_name, schema_name)
        self.assertEqual(data_serie.table_name, table_name)
        self.assertEqual(data_serie.db, db)
        self.assertEqual(data_serie.serie, serie)

@mock.patch('src.serie_date.logics.DateColumn.is_serie_none')
class TestIsdfnone(unittest.TestCase):
    def test_empty(self, mock_none):
        mock_none.return_value = 'The serie is empty'
        serie = DateColumn(None, None, None, None, None)
        result = serie.is_serie_none()
        expect = 'The serie is empty'
        self.assertEqual(result, expect)

    def test_several_null(self, mock_none):
        cnt_null = 2
        mock_none.return_value = f'The serie has {cnt_null} null.'
        serie = DateColumn(None, None, None, None, None)
        result = serie.is_serie_none()
        expect = 'The serie has 2 null.'
        self.assertEqual(result,expect)
        
    def test_no_null(self, mock_none):
        mock_none.return_value = False
        serie = DateColumn(None, None, None, None, None)
        result = serie.is_serie_none()
        self.assertFalse(result)


class TestSetunique(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([1,2,3,4,5,5,6,6], name= 'test')
    def test_set_unique(self):
        self.serie.set_unique()
        result = self.serie.unique
        expect = 6
        self.assertEqual(result, expect)

class TestSetmissing(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([None, None, None, None, 1], name= 'test')
    def test_set_missing(self):
        self.serie.set_missing()
        result = self.serie.n_missing
        expect = 4
        self.assertEqual(result, expect)


@mock.patch('src.database.logics.PostgresConnector.run_query')
class TestSetmin(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.db = PostgresConnector(None, None, None, None)
    def test_set_min(self, mock_run):
        mock_run.return_value = pd.DataFrame([1], columns=['min_date'])
        self.serie.set_min()
        result = self.serie.col_min
        expect = pd.Timestamp('1970-01-01 00:00:00.000000001')
        self.assertEqual(result, expect)

class TestSetmax(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([1,2,3,4,5,5,6,6], name= 'test')
        self.serie.set_max()
        result = self.serie.col_max
        expect = 6
        self.assertEqual(result, expect)

@mock.patch('src.database.logics.PostgresConnector.run_query')
class TestSetweekend(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.db = PostgresConnector(None, None, None, None)

    def test_set_weekend(self, mock_run):
        mock_run.return_value = pd.DataFrame([1], columns=['count'])
        self.serie.set_weekend()
        result = self.serie.n_weekend
        expect = 1
        self.assertEqual(result, expect)
        

class TestSetweekday(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([1,2,3,4,5,6,7], name='test')
        self.serie.n_weekend = 2

    def test_set_weekday(self):
        self.serie.set_weekday()
        result = self.serie.n_weekday
        expect = 5
        self.assertEqual(result, expect)

class TestSetfuture(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([datetime.datetime(2000,1,1,1,1), datetime.datetime(2000,2,3,1,1), datetime.datetime(2033,4,4,1,1)], name='test')
    
    def test_set_future(self):
        self.serie.set_future()
        result = self.serie.n_future
        expect = 1
        self.assertEqual(result, expect)

@mock.patch('src.database.logics.PostgresConnector.run_query')
class TestSetempty(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.db = PostgresConnector(None, None, None, None)
    
    def test_set_empty(self, mock_run):
        mock_run.return_value = pd.DataFrame([1], columns= ['count'])
        self.serie.set_empty_1900()
        result = self.serie.n_empty_1900
        expect = 1
        self.assertEqual(result, expect)

class TestSetempty(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([datetime.date(1970,1,1),
                                      datetime.date(1970,1,1),
                                      datetime.date(1970,1,1),
                                      datetime.date(1970,1,2) ],
                                      name= 'test')
    def test_set_1970(self):
        self.serie.set_empty_1970()
        result = self.serie.n_empty_1970
        expect = 3
        self.assertEqual(result, expect)

class TestSetfrequent(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([1,1,2,2,3,3,4,4,5,5], name='test')
    def test_set_frequent(self):
        self.serie.set_frequent()
        result = self.serie.frequent
        expect = pd.DataFrame([[1,2,0.2], [2,2,0.2],
                               [3,2,0.2], [4,2,0.2],
                               [5,2,0.2]], columns=['value','occurrence','percentage'])
        pd.testing.assert_frame_equal(result, expect)

class TestGetsummarydf(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
        self.serie.unique = 1
        self.serie.n_missing = 0
        self.serie.n_weekend = 2
        self.serie.n_weekday = 5
        self.serie.n_future = 1
        self.serie.n_empty_1900 = 0
        self.serie.n_empty_1970 = 0
        self.serie.col_min = 0
        self.serie.col_max = 1
    def test_get_summary(self):
        result = self.serie.get_summary_df()
        expect = pd.DataFrame([['Number of Unique Values', '1'],
                            ['Number of Rows with Missing Values', '0'],
                            ['Number of Weekend Dates', '2'],
                            ['Number of Weekday Dates', '5'],
                            ['Number of Dates in Future', '1'],
                            ['Number of Rows with 1900-01-01', '0'],
                            ['Number of Rows with 1970-01-01', '0'],
                            ['Minimum Value','0'],
                            ['Maximum Value', '1']],
                            columns= ['Description', 'Value'])
        pd.testing.assert_frame_equal(result, expect)

@mock.patch('src.serie_date.logics.DateColumn.set_unique')
@mock.patch('src.serie_date.logics.DateColumn.set_missing')
@mock.patch('src.serie_date.logics.DateColumn.set_min')
@mock.patch('src.serie_date.logics.DateColumn.set_max')
@mock.patch('src.serie_date.logics.DateColumn.set_weekend')
@mock.patch('src.serie_date.logics.DateColumn.set_weekday')
@mock.patch('src.serie_date.logics.DateColumn.set_future')
@mock.patch('src.serie_date.logics.DateColumn.set_empty_1900')
@mock.patch('src.serie_date.logics.DateColumn.set_empty_1970')
@mock.patch('src.serie_date.logics.DateColumn.set_barchart')
@mock.patch('src.serie_date.logics.DateColumn.set_frequent')
class TestSetdata(unittest.TestCase):
    def setUp(self):
        self.serie = DateColumn(None, None, None, None, None)
    def test_set_data(self,mock_1,mock_2,mock_3,mock_4,mock_5,mock_6,mock_7,mock_8,mock_9,mock_10,mock_11):
        self.serie.set_data()
        assert mock_1.called
        assert mock_2.called
        assert mock_3.called
        assert mock_4.called 
        assert mock_5.called
        assert mock_6.called
        assert mock_7.called
        assert mock_8.called
        assert mock_9.called
        assert mock_10.called
        assert mock_11.called



if __name__ == '__main__':
    unittest.main(verbosity=2)