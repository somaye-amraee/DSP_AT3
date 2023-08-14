def get_negative_number_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_negative_number_query (method): Function that returns the query used for 
    computing the number of times a column from a Postgres table has negative values 
    --------------------
    Parameters
    --------------------
    schema_name(str): The schema name of the selected table in the target database
    table_name(str): The table name of the selected table in the target database
    col_name(str): The column name of the selected column in the target database
    --------------------
    Pseudo-Code
    --------------------
    The query to retrieve the number of negative values in the column
    --------------------
    Returns
    --------------------
    (str): SQL query to get the the number of negative values in the serie
    """
       
    return f'select  count({col_name}) as count from {schema_name}.{table_name} where {col_name} < 0'



def get_std_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_std_query (method): Function that returns the query used for computing the standard deviation value of
     a column from a Postgres table
    --------------------
    Parameters
    --------------------
    schema_name(str): The schema name of the selected table in the target database
    table_name(str): The table name of the selected table in the target database
    col_name(str): The column name of the selected column in the target database
    --------------------
    Pseudo-Code
    --------------------
    The query to retrieve the standard deviation of a column
    --------------------
    Returns
    --------------------
    (str): SQL query to get the standard deviation in the serie
    """
 
    return f'select STDDEV({col_name}) from {schema_name}.{table_name}'

def get_unique_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_unique_query (method): Function that returns the query used for computing the number of
     unique values of a column from a Postgres table
    --------------------
    Parameters
    --------------------
    schema_name(str): The schema name of the selected table in the target database
    table_name(str): The table name of the selected table in the target database
    col_name(str): The column name of the selected column in the target database
    --------------------
    Pseudo-Code
    --------------------
    The query to retrieve the number of unique value in the column
    --------------------
    Returns
    --------------------♣
    (str): SQL query to get the uniqe value in the serie
    """
    return f'select count (distinct {col_name}) from {schema_name}.{table_name}'