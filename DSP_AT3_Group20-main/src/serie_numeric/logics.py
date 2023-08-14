from numpy import average
import streamlit as st
import pandas as pd
import altair as alt

from src.database.logics import PostgresConnector
from src.serie_numeric.queries import get_negative_number_query, get_std_query, get_unique_query

class NumericColumn:
    """
    --------------------
    Description
    --------------------
    -> NumericColumn (class): Class that manages a column loaded from Postgres

    --------------------
    Attributes
    --------------------
    -> schema_name (str): Name of the dataset schema (mandatory)
    -> table_name (str): Name of the dataset table (mandatory)
    -> col_name (str): Name of the column (mandatory)
    -> db (PostgresConnector): Instantation of PostgresConnector class for handling Postgres connection (mandatory)
    -> serie (pd.Series): Pandas serie where the content of a column has been loaded (mandatory)
    -> n_unique (int): Number of unique value of a serie (optional)
    -> n_missing (int): Number of missing values of a serie (optional)
    -> col_mean (int): Average value of a serie (optional)
    -> col_std (int): Standard deviation value of a serie (optional)
    -> col_min (int): Minimum value of a serie (optional)
    -> col_max (int): Maximum value of a serie (optional)
    -> col_median (int): Median value of a serie (optional)
    -> n_zeros (int): Number of times a serie has values equal to 0 (optional)
    -> n_negatives (int): Number of times a serie has negative values (optional)
    -> histogram (int): Altair histogram displaying the count for each bin value of a serie (optional)
    -> frequent (int): Datframe containing the most frequest value of a serie (optional)

    """
    def __init__(self, schema_name, table_name, col_name ,db , serie):
        self.schema_name=schema_name
        self.table_name = table_name
        self.col_name = col_name
        self.db = db
        self.serie = serie
        self.n_unique = None
        self.n_missing = None
        self.col_mean = None
        self.col_std = None
        self.col_min = None
        self.col_max = None
        self.col_median = None
        self.n_zeros = None
        self.n_negatives = None
        self.histogram = None
        self.frequent = None

    def set_data(self):
        """
        --------------------
        Description
        --------------------
        -> set_data (method): Class method that computes all requested information
         from self.serie to be displayed in the Numeric section of Streamlit app 

        --------------------
        Parameters
        --------------------
       None

        --------------------
        Pseudo-Code
        --------------------
        Call relevant methods to set the attributes

        --------------------
        Returns
        --------------------
        None

        """
        
        self.set_unique()   
        self.set_missing()
        self.set_zeros()
        self.set_negatives()
        self.set_mean()
        self.set_std()
        self.set_min()
        self.set_max()
        self.set_median()
        self.set_histogram()
        self.set_frequent()
 

    def is_serie_none(self):
        """
        --------------------
        Description
        --------------------
        -> is_serie_none (method): Class method that checks if self.serie is empty or none 

        --------------------
        Parameters
        --------------------
       None

        --------------------
        Pseudo-Code
        --------------------
        => Create a variable to store the number of null cells in the dataframe
        If statement is to print the relevant information if the dataframe is empty,
        however, print relevent information if the number of null values in the dataframe is not 0,
        if neither, return False 

        --------------------
        Returns
        --------------------
       (str): Relevant information 
        False(boolean): Indicates the dataframe is neither empty or has null

        """
        #=> To be filled by student
        cnt_null = pd.isnull(self.serie).sum()
        if self.df.empty == True: 
            print('The serie is empty')
        elif cnt_null != 0:
            print(f'The serie has {cnt_null} null.')
        else:
            return False

     

    def set_unique(self):
        """
        --------------------
        Description
        --------------------
        -> set_unique (method): Class method that computes the number of unique value of a column using a SQL query (get_unique_query())

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        => To be filled by student
        -> pseudo-code
        --------------------------
        Call get_unique_query method from serie_numeric/queries.py and set the attribute
        --------------------
        Returns
        --------------------
        None

        """
        self.unique =self.db.run_query(get_unique_query(self.schema_name, self.table_name, self.col_name)).iloc[0]['count']
        # self.n_unique = # find the size of the result 
        # st.write(rows)

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        -> set_missing (method): Class method that computes the number of missing value of a serie

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Sum the count of the null value in the pandas serie and set the corresponding attribute

        --------------------
        Returns
        --------------------
        None

        """
        #=> To be filled by student
        self.n_missing = pd.isnull(self.serie).sum()

    def set_zeros(self):
        """
        --------------------
        Description
        --------------------
        -> set_zeros (method): Class method that computes the number of times a serie has values equal to 0

        --------------------
        Parameters
        --------------------
       None

        --------------------
        Pseudo-Code
        --------------------
        Get sum of values of the dataframe which are equal to 0
        Set the attribute

        --------------------
        Returns
        --------------------
       None

        """
        self.n_zeros = (self.serie == 0).sum()

    def set_negatives(self):
        """
        --------------------
        Description
        --------------------
        -> set_negatives (method): Class method that computes the number of times a serie has negative values using a SQL query (get_negative_number_query())

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Run the relevant query in the database class
        Get the value of the dataframe result
        Set the attribute 


        --------------------
        Returns
        --------------------
        None

        """
        #=> To be filled by student
        self.n_negatives = self.db.run_query(get_negative_number_query(self.schema_name, self.table_name, self.col_name)).iloc[0]['count']

    def set_mean(self):
        """
        --------------------
        Description
        --------------------
        -> set_mean (method): Class method that computes the average value of a serie

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Mean function to get the average value in that data.serie and set the relevant attribute

        --------------------
        Returns
        --------------------
        None

        """
        #=> To be filled by student
        self.col_mean = average(self.serie)

    def set_std(self):
        """
        --------------------
        Description
        --------------------
        -> set_std (method): Class method that computes the standard deviation value of a serie using a SQL query (get_std_query)

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Run the relevant query in the database class 
        Get the value of the dataframe result
        Set the attribute

        --------------------
        Returns
        --------------------
        None

        """
        #=> To be filled by student
        self.col_std = self.db.run_query(get_std_query(self.schema_name, self.table_name, self.col_name)).iloc[0]['stddev']
    
    def set_min(self):
        """
        --------------------
        Description
        --------------------
        -> set_min (method): Class method that computes the minimum value of a serie

        --------------------
        Parameters
        --------------------
       None

        --------------------
        Pseudo-Code
        --------------------
        Min function to get the minimum value in that data.serie and set the relevant attribute

        --------------------
        Returns
        --------------------
        None

        """
        #=> To be filled by student
        self.col_min = min(self.serie)

    def set_max(self):
        """
        --------------------
        Description
        --------------------
        -> set_max (method): Class method that computes the maximum value of a serie

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Max function to get the maximum value in that data.serie and set the relevant attribute

        --------------------
        Returns
        --------------------
        None

        """
        #=> To be filled by student
        self.col_max = max(self.serie)

    def set_median(self):
        """
        --------------------
        Description
        --------------------
        -> set_median (method): Class method that computes the median value of a serie

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Median function to get the median value in that data.serie and set the relevant attribute

        --------------------
        Returns
        --------------------
        None

        """
        #=> To be filled by student
        self.col_median = self.serie.median()

    def set_histogram(self):
        """
        --------------------
        Description
        --------------------
        -> set_histogram (method): Class method that computes the Altair histogram displaying the count for each bin value of a serie

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Get a dataframe which store the count of unique values in the serie
        Reset the index for convenience of plotting
        Use altair package to plot a histogram and set the attribute

        --------------------
        Returns
        --------------------
        None

        """
        df = pd.DataFrame(self.serie.value_counts())
        df = df.reset_index()
        self.histogram = alt.Chart(df).mark_bar().encode(
            x = alt.X('index', title =f'{self.col_name}'),
            y = alt.Y(f'{self.col_name}', title = 'Count of Records')
        ).transform_bin(f'{self.col_name}', field = f'{self.col_name}', bin = alt.Bin(maxbins=50))      

    def set_frequent(self, end=20):
        """
        --------------------
        Description
        --------------------
        -> set_frequent (method): Class method that computes the Dataframe containing the most frequest value of a serie

        --------------------
        Parameters
        --------------------
        end(int): The number of dataframe rows that user wants to inspect 

        --------------------
        Pseudo-Code
        --------------------
        Create data frame using value_counts method
        Reset the index 
        Rename column names
        For every value occurrence, divide it by the sum of all occurrence
        Get the end count of rows and store it as df
        Set the attribute

        --------------------
        Returns
        --------------------
        None

        """
        #=> To be filled by student
        df = pd.DataFrame(self.serie.value_counts())
        df = df.reset_index()
        df.columns = ['value', 'occurrence']
        for i in range(len(df.occurrence)):
            df.loc[i,'percentage'] = df.loc[i,'occurrence'] / sum(df.occurrence)
        df = df.head(end)
        self.frequent = df 

    def get_summary_df(self):
        """
        --------------------
        Description
        --------------------
        -> get_summary_df (method): Class method that formats all requested information from self.serie to be displayed in the Overall section of Streamlit app as a Pandas dataframe with 2 columns: Description and Value

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Create a dataframe and show every requested information
        Convert the dataframe values into string

        --------------------
        Returns
        --------------------
        (dataframe): The dataframe shows all the requested information in string format 

        """
        df = pd.DataFrame([['Number of Unique Values', self.unique],
                    ['Number of Rows with Missing Values', self.n_missing],
                    ['number of Rows with 0', self.n_zeros],
                    ['number of Rows with Negative Values', self.n_negatives],
                    ['Average Value', self.col_mean],
                    ['Standard Deviation Value', self.col_std],
                    ['Minimum Value', self.col_min],
                    ['Maximum Value', self.col_max],
                    ['Median Value', self.col_median]],
                    columns= ['Description', 'Value'])  
        return df.astype(str)

        

         