from numpy import shape
import pandas as pd
from itertools import chain
from src.dataframe.queries import get_numeric_tables_query, get_text_tables_query, get_date_tables_query, get_primary_key


class Dataset:
    """
    --------------------
    Description
    --------------------
    -> Dataset (class): Class that manages a dataset loaded from Postgres

    --------------------
    Attributes
    --------------------
    -> schema_name (str): Name of the dataset schema (mandatory)
    -> table_name (str): Name of the dataset table (mandatory)
    -> db (PostgresConnector): Instantation of PostgresConnector class for handling Postgres connection (mandatory)
    -> df (pd.Dataframe): Pandas dataframe where the table content has been loaded (mandatory)
    -> n_rows (int): Number of rows of dataset (optional)
    -> n_cols (int): Number of columns of dataset (optional)
    -> n_duplicates (int): Number of duplicated rows of dataset (optional)
    -> n_missing (int): Number of missing values of dataset (optional)
    -> num_cols (list): List of columns of numerical type (optional)
    -> text_cols (list): List of columns of text type (optional)
    -> date_cols (list): List of columns of datetime type (optional)
    """
    def __init__(self, schema_name=None, table_name=None, db=None, df=None):
        self.schema_name = schema_name
        self.table_name = table_name
        self.db = db
        self.df = df
        self.n_rows = None 
        self.n_cols = None
        self.n_duplicates = None
        self.n_missing = None
        self.num_cols = None
        self.text_cols = None
        self.date_cols = None

    def set_data(self):
        """
        --------------------
        Description
        --------------------
        -> set_data (method): Class method that computes all requested information from self.df to be displayed in the Overall section of Streamlit app 

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Call relevant method of the class to set the attributes' values 

        --------------------
        Returns
        --------------------
        None

        """
        self.set_numeric_columns()
        self.set_text_columns()
        self.set_date_columns()
        self.set_dimensions()
        self.set_duplicates()
        self.set_missing()
        self.set_text_columns()
        
    def is_df_none(self):
        """
        --------------------
        Description
        --------------------
        -> is_df_none (method): Class method that checks if self.df is empty or none 

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Create variable to sum the count of missing values in the dataframe
        If the dataframe is empty, print the information
        If the there is any missing value, print the count of missing values 
        Or return false indicates the dataframe is neither empty or has missing value

        --------------------
        Returns
        --------------------
        'the dataframe is empty'
        'the dataframe has count of nulls'
        False: The dataframe is neither empty or has missing value

        """
        cnt_null = pd.isnull(self.df).sum().sum() 
        if self.df.empty == True: 
            print('The dataframe is empty')
        elif cnt_null != 0:
            print(f'The dataframe has {cnt_null} null.')
        else:
            return False

    def set_dimensions(self):
        """
        --------------------
        Description
        --------------------
        -> set_dimensions (method): Class method that computes the dimensions (number of columns and rows) of self.df and store them as attributes (self.n_rows, self.n_cols)

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Use index 0 of dataframe shape to retrieve count of rows of the dataframe 
        Use index 1 of dataframe shape to retrieve count of columns of the dataframe

        --------------------
        Returns
        --------------------
        None

        """
        self.n_rows = shape(self.df)[0]
        self.n_cols = shape(self.df)[1]

    def set_duplicates(self):
        """
        --------------------
        Description
        --------------------
        -> set_duplicates (method): Class method that computes the number of duplicated of self.df and store it as attribute (self.n_duplicates)

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Sum the count of the duplicated rows to set the attribute

        --------------------
        Returns
        --------------------
        None

        """
        self.n_duplicates = self.df.duplicated().sum()

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        -> set_missing (method): Class method that computes the number of missing values of self.df and store it as attribute (self.n_missing)

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Sum the two dimensions of the missing indicators of the dataframe to set the attribute

        --------------------
        Returns
        --------------------
        None

        """
        self.n_missing = pd.isnull(self.df).sum().sum()

    def set_numeric_columns(self):
        """
        --------------------
        Description
        --------------------
        -> set_numeric_columns (method): Class method that extract the list of numeric columns from a table using a SQL query (from get_numeric_tables_query()),
        store it as attribute (self.num_cols) and then convert the relevant columns of self.df accordingly.

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Run query to get the column names of the columns which are in numeric format in the database and set the attribute 
        Create variable to convert the result dataframe into list
        Convert the corresponding columns in the dataframe to integer format
        --------------------
        Returns
        --------------------
        None

        """
        self.num_cols = self.db.run_query(get_numeric_tables_query(self.schema_name, self.table_name))
        self.num_cols = list(chain.from_iterable(self.num_cols.values.tolist()))
        self.df[self.num_cols] = self.df[self.num_cols].fillna(0)
        self.df[self.num_cols] = self.df[self.num_cols].astype('int')

    def set_text_columns(self):
        """
        --------------------
        Description
        --------------------
        -> set_text_columns (method): Class method that extract the list of text columns from a table using a SQL query (from get_numeric_tables_query()),
        store it as attribute (self.text_cols) and then convert the relevant columns of self.df accordingly.

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Run query to get the column names of the columns which are in text format in the database and set the attribute
        Create variable to convert the result dataframe to list 
        Convert the corresponding columns in the dataframe to string datatype 

        --------------------
        Returns
        --------------------
        None

        """
        self.text_cols = self.db.run_query(get_text_tables_query(self.schema_name, self.table_name))
        self.text_cols = list(chain.from_iterable(self.text_cols.values.tolist()))
        self.df[self.text_cols] = self.df[self.text_cols].fillna(' ')
        self.df[self.text_cols] = self.df[self.text_cols].astype('string')

    def set_date_columns(self):
        """
        --------------------
        Description
        --------------------
        -> set_date_columns (method): Class method that extract the list of datetime columns from a table using a SQL query (from get_numeric_tables_query()),
        store it as attribute (self.date_cols) and then convert the relevant columns of self.df accordingly.

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Run query to get the column names of the columns which are in date format in the database and set the attribute 
        Create variable to store the result dataframe as list
        Convert the corresponding columns in the dataframe to date datatype

        --------------------
        Returns
        --------------------
        None

        """
        self.date_cols = self.db.run_query(get_date_tables_query(self.schema_name, self.table_name))
        self.date_cols = list(chain.from_iterable(self.date_cols.values.tolist()))
        self.df[self.date_cols] = self.df[self.date_cols].fillna(pd.Timestamp(0))
        self.df[self.date_cols] = self.df[self.date_cols].astype('datetime64[ns]')

    def get_head(self, n=5):
        """
        --------------------
        Description
        --------------------
        -> get_head (method): Class method that computes the first rows of self.df according to the provided number of rows specified as parameter (default: 5)

        --------------------
        Parameters
        --------------------
        n(int): number of rows the user wants to inspect 

        --------------------
        Pseudo-Code
        --------------------
        Head function to retrieve the first n rows in the dataframe

        --------------------
        Returns
        --------------------
        (dataframe): The first n rows of the dataframe

        """
        return self.df.head(n)

    def get_tail(self, n=5):
        """
        --------------------
        Description
        --------------------
        -> get_tail (method): Class method that computes the last rows of self.df according to the provided number of rows specified as parameter (default: 5)

        --------------------
        Parameters
        --------------------
        n(int): number of rows the user wants to inspect 

        --------------------
        Pseudo-Code
        --------------------
        Tail function to retrieve the las n rows in the dataframe

        --------------------
        Returns
        --------------------
        (dataframe): The last n rows of the dataframe

        """
        return self.df.tail(n)

    def get_sample(self, n=5):
        """
        --------------------
        Description
        --------------------
        -> get_sample (method): Class method that computes a random sample of rows of self.df according to the provided number of rows specified as parameter (default: 5)

        --------------------
        Parameters
        --------------------
        n(int): The number of rows the user wants to inspect 
        --------------------
        Pseudo-Code
        --------------------
        Sample function to get n rows of sample from the dataframe

        --------------------
        Returns
        --------------------
        (dataframe): The n rows sample of the dataframe

        """
        return self.df.sample(n)

    def get_summary_df(self):
        """
        --------------------
        Description
        --------------------
        -> get_summary_df (method): Class method that formats all requested information from self.df to be displayed in the Overall section of Streamlit app as a Pandas dataframe with 2 columns: Description and Value

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Create a dataframe to display the information which needs to be displayed in the streamlit app overall section

        --------------------
        Returns
        --------------------
        => To be filled by student
        -> (type): description

        """
        df1 = pd.DataFrame([
            ['Name of Table', self.table_name],
            ['Number of Rows', self.n_rows],
            ['Number of Columns', self.n_cols],
            ['Number of Duplicated Rows', self.n_duplicates],
            ['Number of Rows with Missing Values', self.n_missing]],
            columns= ['Description', 'Value'])

        return df1


