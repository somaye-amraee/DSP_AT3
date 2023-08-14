from src import database
import streamlit as st
import pandas as pd
import altair as alt

from src.database.logics import PostgresConnector
from src.serie_text.queries import get_missing_query, get_mode_query, get_alpha_query

class TextColumn:
    """
    --------------------
    Description
    --------------------
    -> TextColumn (class): Class that manages a column loaded from Postgres

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
    -> n_empty (int): Number of times a serie has empty value (optional)
    -> n_mode (int): Mode value of a serie (optional)
    -> n_space (int): Number of times a serie has only space characters (optional)
    -> n_lower (int): Number of times a serie has only lowercase characters (optional)
    -> n_upper (int): Number of times a serie has only uppercase characters (optional)
    -> n_alpha (int): Number of times a serie has only alphabetical characters (optional)
    -> n_digit (int): Number of times a serie has only digit characters (optional)
    -> barchart (int): Altair barchart displaying the count for each value of a serie (optional)
    -> frequent (int): Datframe containing the most frequest value of a serie (optional)

    """
    def __init__(self, schema_name=None, table_name=None, col_name=None, db=None, serie=None):
        self.schema_name = schema_name
        self.table_name = table_name
        self.col_name = col_name
        self.db = db
        self.serie = serie
        self.n_unique = None
        self.n_missing = None
        self.n_empty = None
        self.n_mode = None
        self.n_space = None
        self.n_lower = None
        self.n_upper = None
        self.n_alpha = None
        self.n_digit = None
        self.barchart = None
        self.frequent = None

    
    def set_data(self):
        """
        --------------------
        Description
        --------------------
        -> set_data (method): Class method that computes all requested information from self.serie to be displayed in the Text section of Streamlit app 

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        Gathering the methods contained within the TextColumn class 

        --------------------
        Returns
        --------------------

        """

        self.set_unique()
        self.set_missing()
        self.set_empty()
        self.set_mode()
        self.set_whitespace()
        self.set_lowercase()
        self.set_uppercase()
        self.set_alphabet()
        self.set_digit() 
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
        This method is to show if serie has records or not and would print information to the user of the result before commencing any further.


        --------------------
        Pseudo-Code
        --------------------
        Create a object null_count which sums if dataframe is Null
        IF the dataframe is empty is True THEN print dataframe is empty
        ELSE print serie has number of nulls in the dataframe

        --------------------
        Returns
        --------------------
        Boolean: The result will be printed to say if the dataframe is empty or dataframe has a number of Null values in the dataframe.
        

        """
 
        cnt_null = pd.isnull(self.serie).sum()
        if self.df.empty == True: 
            print(f'The serie is empty')
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
        create an object containing number of unique values in the dataframe
        then return the result of the object showing the number of unique values in the dataframe

        --------------------
        Returns
        --------------------
        int: the number of unique values

        """
        self.n_unique = self.serie.nunique()
      

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        -> set_missing (method): Class method that computes the number of missing value of a serie using a SQL query (get_missing_query())

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        
        self.n_missing class attribute contains get_missing_query function from queries.py of schema name, table name and column name 
        then return the results of the missing values from the create object 

        --------------------
        Returns
        --------------------
        
        int: the number of missing value in the dataframe

        """
    
        # return self.serie.isna.sum()
        self.n_missing = self.db.run_query(get_missing_query(self.schema_name,self.table_name,self.col_name)).iloc[0]['count'] 
        # return f'{self.n_missing} number of missing values in {self.serie}'

    def set_empty(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty (method): Class method that computes the number of times a serie has empty value

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        create an object containing if dataframe has null values
        then return the output of the result of null values from the created object

        --------------------
        Returns
        --------------------
        int: the number of null values in the dataframe

        """
        self.n_empty = self.serie.isnull().sum()
        # return f'{self.n_empty} number of null values in {self.serie}'

    def set_mode(self):
        """
        --------------------
        Description
        --------------------
        -> set_mode (method): Class method that computes the mode value of a serie using a SQL query (get_mode_query())

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        
        class attribute self.n_mode contains get_mode_query function from queries.py of schema name, table name and column name 
        then return the results of the number of frequent values from the class atribute self.n_mode

        --------------------
        Returns
        --------------------
        int: returns a number of the most frequent occurring number from the dataframe

        """

        self.n_mode = self.db.run_query(get_mode_query(self.schema_name,self.table_name,self.col_name)).iloc[0]['mode'] 
        # return f'{self.n_mode} is the most frequent occurring  value in {self.serie}'
        

    def set_whitespace(self):
        """
        --------------------
        Description
        --------------------
        -> set_whitespace (method): Class method that computes the number of times a serie has only space characters

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        class attribute self.n_space equals dataframe count of white spaces
        return result from self.n_space on the number of white spaces in the dataframe

        --------------------
        Returns
        --------------------
        
        int: returns the number of white spaces from the dataframe

        """
        count=0
        for a in self.serie:
            if a is not None:
                if a.isspace() == True:
                    count+=1
                else: 
                    count+=0
                
        self.n_space = count

        # self.n_space = self.serie.str.isspace().sum()
        

        # return f'{self.n_space} number of counts with only space characters in {self.serie}'

    def set_lowercase(self):
        """
        --------------------
        Description
        --------------------
        -> set_lowercase (method): Class method that computes the number of times a serie has only lowercase characters

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        class attribute self.n_lower represents count of lowercase letters within the dataframe
        return result from self.n_lower on the number of lowercase letters in the dataframe

        --------------------
        Returns
        --------------------
        int: returns the numbrer lowercase letters from the dataframe

        """
        self.n_lower = self.serie.str.contains(r'[a-z]').sum()
   

    def set_uppercase(self):
        """
        --------------------
        Description
        --------------------
        -> set_uppercase (method): Class method that computes the number of times a serie has only uppercase characters

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        class attribute self.n_upper represents a count of uppercase letters within the dataframe
        returns result of the number of uppercase letters of the dataframe 

        --------------------
        Returns
        --------------------
        int: returns the numbrer uppercase letters from the dataframe

        """
        # => To be filled by student
        # self.n_upper = self.serie.str.count(r'[A-Z]')
        self.n_upper = self.serie.str.contains(r'[A-Z]').sum()
        # return f'{self.n_upper} number of upper case letters in {self.serie}'
        #self.n_upper = self.serie.str.findall(r'[A-Z]').str.len()
        #or
        #self.n_upper = self.serie.str.count(r'[A-Z]')

    def set_alphabet(self):
        """
        --------------------
        Description
        --------------------
        -> set_alphabet (method): Class method that computes the number of times a serie has only alphabetical characters using a SQL query (get_alpha_query())

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        class attribute self.n_alpha using get_alpha_query from queries.py containing schema name, table name and col name to find the count of alphabetical letters appearing in 
        the dataframe.
        Return the results in self.n_alpha of the count of alphabetical letters appearing in the dataframe.

        --------------------
        Returns
        --------------------
        The count of alphabetical letters 

        """
         
        self.n_alpha = self.db.run_query(get_alpha_query(self.schema_name, self.table_name, self.col_name)).iloc[0]['count'] 



    def set_digit(self):
        """
        --------------------
        Description
        --------------------
        -> set_digit (method): Class method that computes the number of times a serie has only digit characters

        --------------------
        Parameters
        --------------------
        None

        --------------------
        Pseudo-Code
        --------------------
        self.n_digits represents the sum of digits appearing in the dataframe (using loop)
        return results from from self.n_digits 

        --------------------
        Returns
        --------------------
        the final result of the number of digits appearing in the dataframe

        """
        count = 0
        try:
            for a in self.serie:
                if a.isdigit()== True:
                    count+=1
        except:
             count+=0
        

        self.n_digit = count
        # self.n_digit =  sum(c.isdigit() for c in self.serie)


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
        Save the count for each value of a serie as a dataframe and name it 'df'
        reset the index of the dataframe df
        setup a barchart using Altair package 
        

        --------------------
        Returns
        --------------------
        None


        """

        df = pd.DataFrame(self.serie.value_counts())
        df = df.reset_index()
        self.barchart = alt.Chart(df).mark_bar().encode(
            x = alt.X('index', title =f'{self.col_name}'),
            y = alt.Y(f'{self.col_name}', title='Count of Records')
        )        

        # df = pd.DataFrame(self.serie.value_counts())
        # df = df.reset_index()
        # self.barchart = alt.Chart(df).mark_bar().encode(
        #     x = alt.X(f'{self.col_name}', title =f'{self.col_name}'),
        #     y = alt.Y('count()', title='Count of Records')
        # )
        
      
    def set_frequent(self, end=20):
        """
        --------------------
        Description
        --------------------
        -> set_frequent (method): Class method that computes the Dataframe containing the most frequest value of a serie

        --------------------
        Parameters
        --------------------
        20 records to be shown from the result of this method 

        --------------------
        Pseudo-Code
        --------------------
        put all the frequent values into a pandas dataframe and save it as object df
        reset the index of the dataframe in df
        name two columns as 'value' and 'occurrence' in df
        create a loop for each value in occurrence the new column name 'percentage' in df = the value of occurrence / total sum of the occurence
        show only 20 records of df dataframe as save it to the self attribute self.frequent
         


        --------------------
        Returns
        --------------------
        dataframe with columns the value, occurance and percentage.

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
        Dataframe will show:
        Number of Unique Values (self.n_unique),
        Number of Rows with Missing Values (self.n_missing),
        Number of Empty Rows (self.n_empty),
        Number of Rows with Only Whitespaces (self.n_space),
        Number of Rows with Only Lowercases (self.n_lower) ,
        Number of Rows with Only Uppercases (self.n_upper),
        Number of Rows with Only alphabet (self.n_alpha),
        Number of Rows with Only digits (self.n_digit)
        with  dataframe column names [Description, value] 

        --------------------
        Returns
        --------------------
        This output will show all the information requested by the methods into a dataframe

        """
        df = pd.DataFrame([['Number of unique values', self.n_unique],
                        ['Number of missing values', self.n_missing],
                        ['Number of Rows with empty string', self.n_empty],
                        ['Number of Rows with only whitespaces', self.n_space],
                        ['Number of Rows with only lowercases', self.n_lower],
                        ['Number of Rows with only uppercases', self.n_upper],
                        ['Number of Rows with only alphabet', self.n_alpha],
                        ['Number of Rows with only numbers as characters', self.n_digit],
                        ['The mode value',self.n_mode]],
                        columns= ['Description', 'Value'])

        return df.astype(str)

 