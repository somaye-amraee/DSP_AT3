import psycopg2
import pandas as pd

from src.database.queries import get_tables_list_query, get_table_data_query, get_table_schema_query
from src.dataframe.queries import get_primary_key
class PostgresConnector:
    """
    --------------------
    Description
    --------------------
    -> PostgresConnector (class): Class that manages the connection to a Postgres database

    --------------------
    Attributes
    --------------------
    -> database (str): Name of Postgres database (mandatory)
    -> user (str): Username used for connecting to Postgres database (mandatory)
    -> password (str): Password used for connecting to Postgres database (mandatory)
    -> host (str): URL of Postgres database (mandatory)
    -> port (str): Port number of Postgres database (mandatory)
    -> conn (psycopg2._psycopg.connection): Postgres connection object (optional)
    -> cursor (psycopg2._psycopg.connection.cursor): Postgres cursor for executing query (optional)
    -> excluded_schemas (list): List containing the names of internal Postgres schemas to be excluded from selection (information_schema, pg_catalog)
    """
    def __init__(self, database="postgres", user='postgres', password='password', host='127.0.0.1', port='5432'):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None
        self.excluded_schemas = ['information_schema', 'pg_catalog']

    
    def open_connection(self):
        """
        --------------------
        Description
        --------------------
        -> open_connection (method): Class method that creates an active connection to a Postgres database

        --------------------
        Parameters
        --------------------
        No parameter

        --------------------
        Pseudo-Code
        --------------------
        -> If there is any existing connection, close it. The self.conn is not None when the previous attempt to connect is successful.
        -> Create a connection to database using menu's information such as username, password, host, port, database. 
        -> Store the connection in the conn attribute.
        -> If connection failed, a dictionary including status False and error message is returned.
        -> Otherwise, a dictionary including status True and success message is returned.

        --------------------
        Returns
        --------------------
        -> (dict): A dictionary including status and message of the connection. 

        """
        if self.conn != None:
            self.close_connection()
        try:
            self.conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )

        except psycopg2.OperationalError as e:
            return { 'status': False, 'msg': f'Connection to server at {self.host}, port {self.port} failed: {e}' }
        else:
            return { 'status': True, 'msg': 'Connection to database established' }

    def close_connection(self):
        """
        --------------------
        Description
        --------------------
        -> close_connection (method): Class method that closes an active connection to a Postgres database

        --------------------
        Parameters
        --------------------
        No parameter

        --------------------
        Pseudo-Code
        --------------------
        -> Close the existing connection. 

        --------------------
        Returns
        --------------------
        -> (None)

        """
        self.conn.close()

    def open_cursor(self):
        """
        --------------------
        Description
        --------------------
        -> open_cursor (method): Class method that creates an active cursor to a Postgres database 

        --------------------
        Parameters
        --------------------
        No parameter

        --------------------
        Pseudo-Code
        --------------------
        -> Create a cursor from the existing connection object to execute a Postgres command. 
        -> Store the cursor in cursor attribute. 

        --------------------
        Returns
        --------------------
        -> (None)

        """
        self.cursor = self.conn.cursor()
        
    def close_cursor(self):
        """
        --------------------
        Description
        --------------------
        -> close_cursor (method): Class method that closes an active cursor to a Postgres database 

        --------------------
        Parameters
        --------------------
        No parameter

        --------------------
        Pseudo-Code
        --------------------
        -> Close the existing cursor. 

        --------------------
        Returns
        --------------------
        -> (None)

        """
        self.cursor.close()

    def run_query(self, sql_query):
        """
        --------------------
        Description
        --------------------
        -> run_query (method): Class method that executes a SQL query and returns the result as a Pandas dataframe

        --------------------
        Parameters
        --------------------
        -> sql_query (str): The sql command that will be executed.

        --------------------
        Pseudo-Code
        --------------------
        -> Create an active cursor to a Postgres using open_cursor()
        -> Execute the sql_query.
        -> There are two scenarios after running the query:
        If query is executed successfully:
        -> Fetch all the rows returned by the execution using fetchall().
        -> Get the list of column names.
        -> Close the cursor. 
        -> Return the result as a Pandas dataframe. 
        Otherwise:
        -> Close the cursor.
        -> Return an empty Pandas dataframe.

        --------------------
        Returns
        --------------------
        -> (pandas.DataFrame): The result of sql query as a Pandas dataframe.

        """
        try:
            self.open_cursor()
            self.cursor.execute(sql_query)
        except psycopg2.OperationalError as e:
            self.close_cursor()
            return pd.DataFrame([], columns=[])
        else:
            raw_results = self.cursor.fetchall()
            col_names = [desc[0] for desc in self.cursor.description]
            self.close_cursor()
            return pd.DataFrame(raw_results, columns=col_names)

    def list_tables(self):
        """
        --------------------
        Description
        --------------------
        -> list_tables (method): Class method that extracts the list of available tables using a SQL query (get_tables_list_query())

        --------------------
        Parameters
        --------------------
        No parameter

        --------------------
        Pseudo-Code
        --------------------
        -> Call get_tables_list_query() to get the query that extracts all schemas and their tables.
        -> Execute the query. 
        -> Return the result. 

        --------------------
        Returns
        --------------------
        -> (pandas.DataFrame): The list of schemas and their tables as a Pandas dataframe. 

        """
        return self.run_query(get_tables_list_query())

    def load_table(self, schema_name, table_name):
        """
        --------------------
        Description
        --------------------
        -> load_table (method): Class method that load the content of a table using a SQL query (get_table_data_query())

        --------------------
        Parameters
        --------------------
        -> schema_name (str): Name of the selected schema.
        -> table_name  (str): Name of the selected table.

        --------------------
        Pseudo-Code
        --------------------
        -> Call get_table_data_query() to get the query that extracts content of the Postgres table.
        -> Execute the query. 
        -> Return the result.

        --------------------
        Returns
        --------------------
        -> (pandas.DataFrame): The content of the selected table. 

        """
        return self.run_query(get_table_data_query(schema_name, table_name))

    def get_table_schema(self, schema_name, table_name):
        """
        --------------------
        Description
        --------------------
        -> get_table_schema (method): Class method that extracts the schema information of a table using a SQL query (get_table_schema_query())

        --------------------
        Parameters
        --------------------
        -> schema_name (str): Name of the selected schema.
        -> table_name  (str): Name of the selected table.

        --------------------
        Pseudo-Code
        --------------------
        -> Call get_table_schema_query() to get the query that extracts the schema information of the selected table.
        -> Execute the query. 
        -> Return the result.

        --------------------
        Returns
        --------------------
        -> (pandas.DataFrame): Schema information of the selected table.

        """
        df = self.run_query(get_table_schema_query(schema_name, table_name))
        df = df[['table_name', 'column_name', 'data_type', 'is_nullable','character_maximum_length', 'numeric_precision', 'datetime_precision']]
        df3 = self.run_query(get_primary_key(schema_name, table_name))
        df3['primary_key'] = 'YES'
        df = pd.merge(df, df3, on='column_name', how='left')
        for i in range(df.shape[0]):
            if df.loc[i,'primary_key'] == 'YES':
                df.loc[i, 'primary_key'] = True
            else:
                df.loc[i, 'primary_key'] = False
        for i in range(df.shape[0]):
            if df.loc[i, 'is_nullable'] == 'YES':
                df.loc[i, 'is_nullable'] = True
            else:
                df.loc[i, 'is_nullable'] = False
        return df 
