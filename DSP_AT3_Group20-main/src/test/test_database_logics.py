import os
from cmath import nan
import sys
import unittest
from unittest import mock
import pandas as pd
import pandas.testing as pd_testing
import psycopg2

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.database.logics import PostgresConnector

class TestPostgresConnectorInstantiation(unittest.TestCase):
    """
    Class used for testing the instanciation of the PostgresConnector class from src/database/logics.py
    """
    def test_postgres_connector_instanciation(self):
        database = 'postgres'
        username = 'postgres'
        password = 'postgrespwd'
        host = 'localhost'
        port = '5432'
        
        postgresConnector = PostgresConnector(database, username, password, host, port)
        self.assertEqual(postgresConnector.database, database)
        self.assertEqual(postgresConnector.user, username)
        self.assertEqual(postgresConnector.password, password)
        self.assertEqual(postgresConnector.host, host)
        self.assertEqual(postgresConnector.port, port)

class TestOpenConnection(unittest.TestCase):
    """
    Class used for testing the PostgresConnector.open_connection() method from src/database/logics.py
    """
    def setUp(self):
        database = 'postgres'
        username = 'postgres'
        password = 'postgrespwd'
        host = 'localhost'
        port = '5432'
        self.postgresConnector = PostgresConnector(database, username, password, host, port)

    #test successful connection
    @mock.patch('psycopg2.connect')
    def test_open_connection_success(self, mock_connect):
        result = self.postgresConnector.open_connection()
        mock_connect.assert_called_with(
            user=self.postgresConnector.user,
            password=self.postgresConnector.password,
            host=self.postgresConnector.host,
            port=self.postgresConnector.port,
            database=self.postgresConnector.database
        )
        self.assertEqual(result['status'], True)
        self.assertEqual(result['msg'], 'Connection to database established')
        self.assertEqual(self.postgresConnector.conn, mock_connect.return_value)

    #test failed connection
    @mock.patch('psycopg2.connect')
    def test_open_connection_failed(self, mock_connect):
        exception_msg = 'Wrong password'
        expected_msg = f'Connection to server at {self.postgresConnector.host}, port {self.postgresConnector.port} failed: {exception_msg}' 

        mock_connect.side_effect = psycopg2.OperationalError(exception_msg)
        result = self.postgresConnector.open_connection()
        mock_connect.assert_called_with(
            user=self.postgresConnector.user,
            password=self.postgresConnector.password,
            host=self.postgresConnector.host,
            port=self.postgresConnector.port,
            database=self.postgresConnector.database
        )
        self.assertEqual(result['status'], False)
        self.assertEqual(result['msg'], expected_msg)
        self.assertEqual(self.postgresConnector.conn, None)

class TestCloseConnection(unittest.TestCase):
    """
    Class used for testing the PostgresConnector.close_connection() method from src/database/logics.py
    """

    def test_close_connection(self):
        mock_conn = mock.MagicMock()
        postgresConnector = PostgresConnector(None, None, None, None, None)
        postgresConnector.conn = mock_conn
        postgresConnector.close_connection()
        mock_conn.close.assert_called()

class TestOpenCursor(unittest.TestCase):
    """
    Class used for testing the PostgresConnector.open_cursor() method from src/database/logics.py
    """
    def test_open_cursor(self):
        mock_con = mock.MagicMock() 
        postgresConnector = PostgresConnector(None, None, None, None, None)
        postgresConnector.conn = mock_con
        postgresConnector.open_cursor()
        mock_con.cursor.assert_called() 
        self.assertEqual(mock_con.cursor.return_value, postgresConnector.cursor)

class TestCloseCursor(unittest.TestCase):
    """
    Class used for testing the PostgresConnector.close_cursor() method from src/database/logics.py
    """
    def test_close_cursor(self):
        mock_cursor = mock.MagicMock()
        postgresConnector = PostgresConnector(None, None, None, None, None)
        postgresConnector.cursor = mock_cursor
        postgresConnector.close_cursor()
        mock_cursor.close.assert_called() 

class TestRunQuery(unittest.TestCase):
    """
    Class used for testing the PostgresConnector.run_query() method from src/database/logics.py
    """

    # test run_query when query execution failed (for example, query is invalid)
    def test_run_query_execution_failed(self):
        mock_con = mock.MagicMock()
        mock_cursor = mock_con.cursor.return_value 
        postgresConnector = PostgresConnector(None, None, None, None, None)
        postgresConnector.conn = mock_con
        mock_cursor.execute.side_effect = psycopg2.OperationalError("Invalid query")
        self.assertTrue(postgresConnector.run_query("select from").empty)
        mock_cursor.close.assert_called()
    
    # test run_query when data returned by the query is not empty.
    # for example, the following query collects all schema + table from a database and there are schemas and tables in the database.
    def test_run_query_not_empty_result(self):
        sample_raw_results = [['public', 'categories'], ['public', 'customers']]
        sample_cursor_desc = (psycopg2.extensions.Column(name='table_schema', type_code=19), psycopg2.extensions.Column(name='table_name', type_code=19))
        expected_output = pd.DataFrame(sample_raw_results, columns=['table_schema', 'table_name'])
        sql_query = "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema not in ('information_schema', 'pg_catalog')"

        mock_con = mock.MagicMock()
        mock_cursor = mock_con.cursor.return_value 
        mock_cursor.fetchall.return_value = sample_raw_results
        mock_cursor.description = sample_cursor_desc
        
        postgresConnector = PostgresConnector(None, None, None, None, None)
        postgresConnector.conn = mock_con
        actual_output = postgresConnector.run_query(sql_query)

        mock_con.cursor.assert_called()
        mock_cursor.execute.assert_called_with(sql_query)
        mock_cursor.fetchall.assert_called()
        mock_cursor.close.assert_called()

        self.assertTrue(expected_output.equals(actual_output))

    # test run_query when data returned by the query is empty.
    # for example, the following query collects all schema + table from a database but there is no table in the database.
    def test_run_query_empty_result(self):
        sample_raw_results = []
        sample_cursor_desc = (psycopg2.extensions.Column(name='table_schema', type_code=19), psycopg2.extensions.Column(name='table_name', type_code=19))
        expected_results = pd.DataFrame(sample_raw_results, columns=['table_schema', 'table_name'])
        sql_query = "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema not in ('information_schema', 'pg_catalog')"

        mock_con = mock.MagicMock()
        mock_cursor = mock_con.cursor.return_value 
        mock_cursor.fetchall.return_value = sample_raw_results
        mock_cursor.description = sample_cursor_desc
        
        postgresConnector = PostgresConnector(None, None, None, None, None)
        postgresConnector.conn = mock_con
        result = postgresConnector.run_query(sql_query)

        mock_con.cursor.assert_called()
        mock_cursor.execute.assert_called_with(sql_query)
        mock_cursor.fetchall.assert_called()
        mock_cursor.close.assert_called()

        self.assertTrue(expected_results.equals(result))

class TestLoadTable(unittest.TestCase):
    """
    Class used for testing the PostgresConnector.load_table() method from src/database/logics.py
    """
    @mock.patch('src.database.logics.PostgresConnector.run_query')
    def test_list_tables(self, mock_run_query):
        schema_name = 'public'
        table_name = 'categories'
        postgresConnector = PostgresConnector(None, None, None, None, None)
        postgresConnector.load_table(schema_name, table_name)

        mock_run_query.assert_called_with(f'SELECT * FROM {schema_name}.{table_name}')

class TestGetTableSchema(unittest.TestCase):
    """
    Class used for testing the PostgresConnector.get_table_schema() method from src/database/logics.py
    """

    # test get_table_schema() when schema name and table name exist in the database -> there is schema information of the table
    @mock.patch("src.database.logics.PostgresConnector.run_query")
    def test_get_table_schema_not_empty(self, mock_run_query):
        schema_name = 'public'
        table_name = 'categories'
        sample_cols_info = pd.DataFrame(
            [
                ['public', 'categories', 'category_id', 'smallint', 'NO', nan, '16.000', nan], 
                ['public', 'categories', 'description', 'text', 'YES', nan, nan, nan]
            
            ], 
            columns=['table_schema', 'table_name', 'column_name', 'data_type', 'is_nullable','character_maximum_length', 'numeric_precision', 'datetime_precision']
        )
        sample_primary_cols = pd.DataFrame(['category_id'], columns=['column_name'])
        expected_results = pd.DataFrame(
            [
                ['categories', 'category_id', 'smallint', False, nan, '16.000', nan, True], 
                ['categories', 'description', 'text', True, nan, nan, nan, False]
            
            ], 
            columns=['table_name', 'column_name', 'data_type', 'is_nullable','character_maximum_length', 'numeric_precision', 'datetime_precision', 'primary_key']
        )
        mock_run_query.side_effect = [sample_cols_info, sample_primary_cols]
        postgresConnector = PostgresConnector(None, None, None, None, None)
        actual_results = postgresConnector.get_table_schema(schema_name, table_name)

        mock_run_query.assert_has_calls([
            mock.call(f"SELECT * FROM information_schema.columns WHERE table_schema = '{schema_name}' and table_name = '{table_name}'"),
            mock.call(f"select c.column_name from information_schema.table_constraints t left join information_schema.constraint_column_usage c on c.constraint_name = t.constraint_name where t.table_schema = '{schema_name}' and t.constraint_type = 'PRIMARY KEY' and t.table_name = '{table_name}'")
        ], any_order=True)
        
        pd_testing.assert_frame_equal(actual_results, expected_results, check_dtype=False)

    # test get_table_schema() when schema name and table name do not exist in the database -> schema information is empty
    @mock.patch("src.database.logics.PostgresConnector.run_query")
    def test_get_table_schema(self, mock_run_query):
        schema_name = 'public1'
        table_name = 'categories1'
        sample_cols_info = pd.DataFrame([], 
            columns=['table_schema', 'table_name', 'column_name', 'data_type', 'is_nullable','character_maximum_length', 'numeric_precision', 'datetime_precision']
        )
        sample_primary_cols = pd.DataFrame([], columns=['column_name'])
        expected_results = pd.DataFrame(
            [], 
            columns=['table_name', 'data_type', 'is_nullable', 'character_maximum_length', 'numeric_precision', 'datetime_precision', 'column_name', 'primary_key']
        )
        mock_run_query.side_effect = [sample_cols_info, sample_primary_cols]
        postgresConnector = PostgresConnector(None, None, None, None, None)
        actual_results = postgresConnector.get_table_schema(schema_name, table_name)

        mock_run_query.assert_has_calls([
            mock.call(f"SELECT * FROM information_schema.columns WHERE table_schema = '{schema_name}' and table_name = '{table_name}'"),
            mock.call(f"select c.column_name from information_schema.table_constraints t left join information_schema.constraint_column_usage c on c.constraint_name = t.constraint_name where t.table_schema = '{schema_name}' and t.constraint_type = 'PRIMARY KEY' and t.table_name = '{table_name}'")
        ], any_order=True)
        
        pd_testing.assert_frame_equal(actual_results, expected_results, check_dtype=False)

if __name__ == '__main__':
    unittest.main(verbosity=2)