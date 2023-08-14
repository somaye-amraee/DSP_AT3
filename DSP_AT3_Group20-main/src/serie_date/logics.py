import datetime
import pandas as pd
import altair as alt

from src.serie_date.queries import get_min_date_query, get_weekend_count_query, get_1900_count_query

class DateColumn:
    """
    --------------------
    Description
    --------------------
    -> DateColumn (class): Class that manages a column loaded from Postgres

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
    -> col_min (int): Minimum value of a serie (optional)
    -> col_max (int): Maximum value of a serie (optional)
    -> n_weekend (int): Number of times a serie has dates falling during weekend (optional)
    -> n_weekday (int): Number of times a serie has dates not falling during weekend (optional)
    -> n_future (int): Number of times a serie has dates falling in the future (optional)
    -> n_empty_1900 (int): Number of times a serie has dates equal to '1900-01-01' (optional)
    -> n_empty_1970 (int): Number of times a serie has dates equal to '1970-01-01' (optional)
    -> barchart (int): Altair barchart displaying the count for each value of a serie (optional)
    -> frequent (int): Dataframe containing the most frequest value of a serie (optional)

    """
    def __init__(self, schema_name=None, table_name=None, col_name=None, db=None, serie=None):
        self.schema_name = schema_name
        self.table_name = table_name
        self.col_name = col_name
        self.db = db
        self.serie = serie
        self.unique = None
        self.n_missing = None
        self.col_min = None
        self.col_max = None
        self.n_weekend = None
        self.n_weekday = None
        self.n_future = None
        self.n_empty_1900 = None
        self.n_empty_1970 = None
        self.barchart = None
        self.frequent = None

    def set_data(self):
        """
        --------------------
        Description
        --------------------
        -> set_data (method): Class method that computes all requested information from self.serie to be displayed in the Date section of Streamlit app 

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
        self.set_min()
        self.set_max()
        self.set_weekend()
        self.set_weekday()
        self.set_future()
        self.set_empty_1900()
        self.set_empty_1970()
        self.set_barchart()
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
        Create a variable to store the number of null cells in the dataframe
        If statement to print the relevant information if the dataframe is empty
        Print relevant information if the number of null values in the dataframe is not 0
        If neither, return False 

        --------------------
        Returns
        --------------------
        (str): Relevant information 
        False(boolean): Indicates the dataframe is neither empty or has null

        """
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
        -> set_unique (method): Class method that computes the number of unique value of a serie

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Call nunique method of pandas serie and set the attribute

        --------------------
        Returns
        --------------------
        None

        """
        self.unique = self.serie.nunique()

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
        => To be filled by student
        -> (type): description

        """
        self.n_missing = pd.isnull(self.serie).sum()

    def set_min(self):
        """
        --------------------
        Description
        --------------------
        -> set_min (method): Class method that computes the minimum value of a serie using a SQL query (get_min_date_query())

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        In the database class run the relevant query to retrieve the minimum value in the serie and store the value in a new variable 
        Convert the minimum value in the column to datetime type and set the relevant attribute

        --------------------
        Returns
        --------------------
        => To be filled by student
        -> (type): description

        """
        col_min = self.db.run_query(get_min_date_query(self.schema_name, self.table_name, self.col_name)).iloc[0]['min_date']
        self.col_min = pd.to_datetime(col_min)

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
        self.col_max = max(self.serie)

    def set_weekend(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekend (method): Class method that computes the number of times a serie has dates falling during weekend using a SQL query (get_weekend_count_query())

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
        self.n_weekend = self.db.run_query(get_weekend_count_query(self.schema_name, self.table_name, self.col_name)).iloc[0]['count']

    def set_weekday(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekday (method): Class method that computes the number of times a serie has dates not falling during weekend

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        The length of the serie minus the number of weekend and set the attribute 

        --------------------
        Returns
        --------------------
        None
        """
        self.n_weekday = len(self.serie) - self.n_weekend

    def set_future(self):
        """
        --------------------
        Description
        --------------------
        -> set_future (method): Class method that computes the number of times a serie has dates falling in the future

        --------------------
        Parameters
        --------------------
        None 

        --------------------
        Pseudo-Code
        --------------------
        Subset the serie to get a dataframe stores only dates larger than today and set the attribute


        --------------------
        Returns
        --------------------
        None

        """
        self.n_future = self.serie[self.serie > datetime.datetime.now()].count()

    def set_empty_1900(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1900 (method): Class method that computes the number of times a serie has dates equal to '1900-01-01' using a SQL query (get_1900_count_query())

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Run the relevant query in the database class 
        Get the value of the result dataframe
        Set the attribute

        --------------------
        Returns
        --------------------
        None

        """
        self.n_empty_1900 = self.db.run_query(get_1900_count_query(self.schema_name, self.table_name, self.col_name)).iloc[0]['count']

    def set_empty_1970(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1970 (method): Class method that computes the number of times a serie has dates equal to '1970-01-01'

        --------------------
        Parameters
        --------------------
        None 

        --------------------
        Pseudo-Code
        --------------------
        Subset the serie to get a serie which has a date value equals to 1970-01-01
        Count the rows of the serie
        Set the attribute

        --------------------
        Returns
        --------------------
        None

        """
        self.n_empty_1970 = self.serie[self.serie == datetime.datetime(1970,1,1)].count()
        
    def set_barchart(self):  
        """
        --------------------
        Description
        --------------------
        -> set_barchart (method): Class method that computes the Altair barchart displaying the count for each value of a serie

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Get a dataframe which store the count of unique values in the serie
        Reset the index for convenience of plotting
        Use altair package to plot a bar chart and set the attribute

        --------------------
        Returns
        --------------------
        None 

        """
        df = pd.DataFrame(self.serie.value_counts())
        df = df.reset_index()
        print(df)
        self.barchart = alt.Chart(df).mark_bar().encode(
            x = alt.X('index', title =f'{self.col_name}'),
            y = alt.Y(f'{self.col_name}', title='Count of Records')
        )

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
                            ['Number of Weekend Dates', self.n_weekend],
                            ['Number of Weekday Dates', self.n_weekday],
                            ['Number of Dates in Future', self.n_future],
                            ['Number of Rows with 1900-01-01', self.n_empty_1900],
                            ['Number of Rows with 1970-01-01', self.n_empty_1970],
                            ['Minimum Value', self.col_min],
                            ['Maximum Value', self.col_max]],
                            columns= ['Description', 'Value'])
        return df.astype(str)
