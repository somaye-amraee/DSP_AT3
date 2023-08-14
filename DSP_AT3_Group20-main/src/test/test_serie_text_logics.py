
import unittest
import pandas as pd
from unittest import mock 
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.serie_text.logics import TextColumn
from src.database.logics import PostgresConnector

# instantiate TextColumn 
@mock.patch('src.database.logics.PostgresConnector')
class Test_TextColumn(unittest.TestCase):
    def test_TextColumn(self,sample_db):
        schema_name = "public"
        table_name = "categories"
        col_name = "description"
        db = sample_db
        serie = sample_db.load_table(schema_name, table_name)[col_name]

        text_param = TextColumn(schema_name, table_name, col_name, db, serie)
        self.assertEqual(text_param.schema_name,schema_name)
        self.assertEqual(text_param.table_name, table_name)
        self.assertEqual(text_param.db, db)
        self.assertEqual(text_param.serie, serie)

# Testing is_serie_none() method in TextColumn class
@mock.patch('src.serie_text.logics.TextColumn.is_serie_none')
class TestIsdfnone(unittest.TestCase):
    def test_empty(self, mock_none):
        mock_none.return_value = 'The serie is empty'
        serie = TextColumn(None, None, None, None, None)
        result = serie.is_serie_none()
        expect = 'The serie is empty'
        self.assertEqual(result, expect)

    def test_several_null(self, mock_none):
        cnt_null = 5
        mock_none.return_value = f'The serie has {cnt_null} null.'
        serie = TextColumn(None, None, None, None, None)
        result = serie.is_serie_none()
        expect = 'The serie has 5 null.'
        self.assertEqual(result,expect)
        
    def test_null_errors(self, mock_none):
        mock_none.return_value = False
        serie = TextColumn(None, None, None, None, None)
        result = serie.is_serie_none()
        self.assertFalse(result)

# Test set_unique() 
@mock.patch('src.database.logics.PostgresConnector')
class TestSetunique(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([12,2,3,4,5,6,7,8,8], name= 'test')
    def test_set_unique(self,fake):
        fake.return_value = pd.DataFrame([1], columns=['count'])
        self.serie.set_unique()
        result = self.serie.n_unique
        expect = 8
        self.assertEqual(result, expect)

##### Missing values

@mock.patch('src.database.logics.PostgresConnector.run_query')
class TestSetmissing(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.db = PostgresConnector(None, None, None, None)
    def test_set_missing(self,sample_db):
        sample_db.return_value = pd.DataFrame([1],columns=['count'])
        self.serie.set_missing()
        result = self.serie.n_missing # the actual result 
        expect = 1 #our sample expectation
        self.assertEqual(result, expect)


# Test set_empty()
class TestSetEmpty(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([None, 3, 2, 1, 12], name= 'count')

    def test_set_empty(self):
        self.serie.set_empty()
        result = self.serie.n_empty
        expect = 1
        self.assertEqual(result, expect)


###### set_mode()

@mock.patch('src.database.logics.PostgresConnector.run_query')
class TestSetMode(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.db = PostgresConnector(None, None, None, None)
    
    def test_set_mode(self, fake):
        fake.return_value = pd.DataFrame([1], columns= ['mode'])
        self.serie.set_mode()
        result = self.serie.n_mode
        expect = 1 # unsure
        self.assertEqual(result, expect)

### whitespace

class TestSetWhitespace(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.serie = pd.Series(['tech', 'fire', ' ', '3', 'wait',' ',' '], name= 'count')
        self.serie.set_whitespace()
        result = self.serie.n_space
        expect = 3
        self.assertEqual(result, expect)

### lowercase

class TestSetLowercase(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.serie = pd.Series(['as','WE','asdf','tech','42'], name= 'count')
        self.serie.set_lowercase()
        result = self.serie.n_lower
        expect = 3
        self.assertEqual(result, expect)

### uppercase

class TestSetUppercase(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.serie = pd.Series(['as','WE','asdf','tech','42',"NOT"], name= 'count')
        self.serie.set_uppercase()
        result = self.serie.n_upper
        expect = 2
        self.assertEqual(result, expect)

## Alphabet

@mock.patch('src.database.logics.PostgresConnector.run_query')
class TestSetalphabet(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.db = PostgresConnector(None, None, None, None)

    def test_set_alphabet(self, fake):
        fake.return_value = pd.DataFrame([1], columns=['count'])
        self.serie.set_alphabet()
        result = self.serie.n_alpha
        expect = 1
        self.assertEqual(result, expect)

### digits

class TestSetDigit(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.serie = pd.Series(['as','WE','34','13','42',"NOT"], name= 'count')
        self.serie.set_digit()
        result = self.serie.n_digit
        expect = 3
        self.assertEqual(result, expect)



class TestSetFrequent(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.serie = pd.Series([1,1,2,2,3,3,4,4,5,5], name='test')
    def test_set_frequent(self):
        self.serie.set_frequent()
        result = self.serie.frequent
        expect = pd.DataFrame([[1,2,0.2], [2,2,0.2],
                               [3,2,0.2], [4,2,0.2],
                               [5,2,0.2]], columns=['value','occurrence','percentage'])
        pd.testing.assert_frame_equal(result, expect)


### Test get summary
class TestGetSummaryDF(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
        self.serie.n_unique = 17
        self.serie.n_missing = 3
        self.serie.n_empty = 2
        self.serie.n_space = 14
        self.serie.n_lower = 34
        self.serie.n_upper = 12
        self.serie.n_alpha = 10
        self.serie.n_digit = 1
        self.serie.n_mode = 3

    def test_get_summary(self):
        result = self.serie.get_summary_df()
        expect = pd.DataFrame([['Number of unique values', '17'],
                            ['Number of missing values', '3'],
                            ['Number of Rows with empty string', '2'],
                            ['Number of Rows with only whitespaces', '14'],
                            ['Number of Rows with only lowercases', '34'],
                            ['Number of Rows with only uppercases', '12'],
                            ['Number of Rows with only alphabet', '10'],
                            ['Number of Rows with only numbers as characters','1'],
                            ['The mode value', '3']],
                            columns= ['Description', 'Value'])
        pd.testing.assert_frame_equal(result, expect)

@mock.patch('src.serie_text.logics.TextColumn.set_unique')
@mock.patch('src.serie_text.logics.TextColumn.set_missing')
@mock.patch('src.serie_text.logics.TextColumn.set_empty')
@mock.patch('src.serie_text.logics.TextColumn.set_mode')
@mock.patch('src.serie_text.logics.TextColumn.set_whitespace')
@mock.patch('src.serie_text.logics.TextColumn.set_lowercase')
@mock.patch('src.serie_text.logics.TextColumn.set_uppercase')
@mock.patch('src.serie_text.logics.TextColumn.set_alphabet')
@mock.patch('src.serie_text.logics.TextColumn.set_digit')
@mock.patch('src.serie_text.logics.TextColumn.set_barchart')
@mock.patch('src.serie_text.logics.TextColumn.set_frequent')
class TestSetdata(unittest.TestCase):
    def setUp(self):
        self.serie = TextColumn(None, None, None, None, None)
    def test_set_data(self,fake_1,fake_2,fake_3,fake_4,fake_5,fake_6,fake_7,fake_8,fake_9,fake_10,fake_11):
        self.serie.set_data()
        assert fake_1.called
        assert fake_2.called
        assert fake_3.called
        assert fake_4.called 
        assert fake_5.called
        assert fake_6.called
        assert fake_7.called
        assert fake_8.called
        assert fake_9.called
        assert fake_10.called
        assert fake_11.called




if __name__ == '__main__':
    unittest.main(verbosity=2)