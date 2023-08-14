import os
from random import seed
import sys
import unittest
from numpy import NAN
import pandas as pd
from unittest import mock

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.dataframe.logics import Dataset

@mock.patch('src.database.logics.PostgresConnector')
class TestDatasetInstantiation(unittest.TestCase):
    def test_dataset_instanciation(self, mock_db):
        schema_name = 'public'
        table_name = 'orders'
        db = mock_db
        df = mock_db.load_table(schema_name, table_name)

        dataset = Dataset('public', 'orders', db, df)
        self.assertEqual(dataset.schema_name, schema_name)
        self.assertEqual(dataset.table_name, table_name)
        self.assertEqual(dataset.db, db)
        self.assertEqual(dataset.df, df)

@mock.patch('src.dataframe.logics.Dataset.is_df_none')
class TestIsdfnone(unittest.TestCase):
    def test_empty(self, mock_none):
        mock_none.return_value = 'The dataframe is empty'
        dataset = Dataset(None, None, None, None)
        result = dataset.is_df_none()
        expect = 'The dataframe is empty'
        self.assertEqual(result, expect)

    def test_several_null(self, mock_none):
        cnt_null = 2
        mock_none.return_value = f'The dataframe has {cnt_null} null.'
        dataset = Dataset(None, None, None, None)
        result = dataset.is_df_none()
        expect = 'The dataframe has 2 null.'
        self.assertEqual(result,expect)
        
    def test_no_null(self, mock_none):
        mock_none.return_value = False
        dataset = Dataset(None, None, None, None)
        result = dataset.is_df_none()
        self.assertFalse(result)


class TestSetdimensions(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset(None, None, None, None)
    def test_n_dimensions(self):
        sample_df = pd.DataFrame([[1,2],[3,4]], columns= ['1','2'])
        self.dataset.df = sample_df
        self.dataset.set_dimensions()
        self.assertEqual(self.dataset.n_cols, 2)
        self.assertEqual(self.dataset.n_rows, 2)
       

class TestSetduplicates(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset(None, None, None, None)
    def test_set_duplicates(self):
        sample_df = pd.DataFrame([[1,2],[1,2],[3,4],[3,4]], columns=['1','2'])
        self.dataset.df = sample_df
        self.dataset.set_duplicates()
        self.assertEqual(self.dataset.n_duplicates, 2)


class TestSetmissing(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset(None, None, None, None)
    def test_set_missing(self):
        sample_df = pd.DataFrame([[1,2,3,4,NAN, NAN],
                                  [1,2,NAN,NAN,NAN,NAN]],
                                  columns=['1','2','3','4','5','6'])
        self.dataset.df = sample_df
        self.dataset.set_missing()
        result = self.dataset.n_missing
        self.assertEqual(result, 6)


@mock.patch('src.database.logics.PostgresConnector')
@mock.patch('pandas.DataFrame')
class TestSetnumeric(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset(None, None, None, None)
    def test_numeric_columns(self, postgresconnector,mock_as):
        self.dataset.db = postgresconnector
        sample_df = pd.DataFrame([['1'],['2'],['3'],['4']], columns=['1'])
        postgresconnector.run_query.return_value = sample_df
        self.dataset.df = pd.DataFrame([[1,2,3,4,5],[6,7,8,9,10]], columns=['1','2','3','4','5'])
        self.dataset.set_numeric_columns()
        self.assertEqual(self.dataset.num_cols, sample_df)


@mock.patch('src.database.logics.PostgresConnector')
@mock.patch('pandas.DataFrame')
class TestSettext(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset(None, None, None, None)
    def test_text_columns(self, postgresconnector, mock_as ):
        self.dataset.db = postgresconnector
        sample_df = pd.DataFrame([['1'],['2'],['3'],['4']], columns=['1'])
        postgresconnector.run_query.return_value = sample_df
        self.dataset.df = pd.DataFrame([[1,2,3,4,5],[6,7,8,9,10]], columns=['1','2','3','4','5'])
        self.dataset.set_text_columns()
        self.assertEqual(self.dataset.text_cols, sample_df)


@mock.patch('src.database.logics.PostgresConnector')
@mock.patch('pandas.DataFrame')
class TestSettext(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset(None, None, None, None)
    def test_date_columns(self, postgresconnector, mock_as):
        self.dataset.db = postgresconnector
        sample_df = pd.DataFrame([['1'],['2'],['3'],['4']], columns=['1'])
        postgresconnector.run_query.return_value = sample_df
        self.dataset.df = pd.DataFrame([[1,2,3,4,5],[6,7,8,9,10]], columns=['1','2','3','4','5'])
        self.dataset.set_date_columns()
        self.assertEqual(self.dataset.date_cols, sample_df)

class TestGet(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset(None, None, None, None)
        self.dataset.df = pd.DataFrame([[1,2],[1,2],[3,4],[3,4]], columns=['1','2'])
    def test_get_head(self):
        seed(42)
        result = self.dataset.get_head(1)
        expect = self.dataset.df.head(1)
        pd.testing.assert_frame_equal(result, expect)

    def test_get_tail(self):
        result = self.dataset.get_tail(1)
        expect = self.dataset.df.tail(1)
        pd.testing.assert_frame_equal(result, expect)

    def test_get_sample(self):
        result = self.dataset.get_sample(1)
        expect = self.dataset.df.sample(1)
        pd.testing.assert_frame_equal(result, expect)

    def test_get_summary(self):
        self.dataset.table_name =1 
        self.dataset.n_rows = 1
        self.dataset.n_cols = 1
        self.dataset.n_duplicates = 1
        self.dataset.n_missing = 1
        result = self.dataset.get_summary_df()
        expect = pd.DataFrame([
            ['Name of Table', 1],
            ['Number of Rows', 1],
            ['Number of Columns', 1],
            ['Number of Duplicated Rows', 1],
            ['Number of Rows with Missing Values', 1]],
            columns= ['Description', 'Value'])
        pd.testing.assert_frame_equal(result, expect)


if __name__ == '__main__':
    unittest.main(verbosity=2)