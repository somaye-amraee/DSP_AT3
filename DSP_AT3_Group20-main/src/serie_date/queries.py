
def get_min_date_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_min_date_query (method): Function that returns the query used for computing the earliest date of a datetime column from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str): The schema name of the selected table in the target database
    table_name(str): The table name of the selected table in the target database
    col_name(str): The column name of the selected column in the target database

    --------------------
    Pseudo-Code
    --------------------
    The query to retrieve the minimum value in the column

    --------------------
    Returns
    --------------------
    (str): SQL query to get the minimum value in the serie

    """
    return f"select min({col_name}) as min_date from {schema_name}.{table_name}"

def get_weekend_count_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_weekend_count_query (method): Function that returns the query used for computing the number of times a date of a datetime column falls during weekends

    --------------------
    Parameters
    --------------------
    schema_name(str): The schema name of the selected table in the target database
    table_name(str): The table name of the selected table in the target database
    col_name(str): The column name of the selected column in the target database

    --------------------
    Pseudo-Code
    --------------------
    The query to retrieve the number of weekend in the column 

    --------------------
    Returns
    --------------------
    (str): SQL query to get the count of weekend dates in the serie

    """
    return f"select count(*) from (select extract(dow from {col_name}) as weekend from {schema_name}.{table_name}) as temp where weekend in (0,6)"

def get_1900_count_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_1900_count_query (method): Function that returns the query used for computing the number of times a datetime column has the value '1900-01-01'

    --------------------
    Parameters
    --------------------
    schema_name(str): The schema name of the selected table in the target database
    table_name(str): The table name of the selected table in the target database
    col_name(str): The column name of the selected column in the target database

    --------------------
    Pseudo-Code
    --------------------
    The query to retrieve the number of date which is 1900-01-01

    --------------------
    Returns
    --------------------
    (str): SQL query to get the count of dates which equals to 1900-01-01

    """
    return f"select count(*) from (select date({col_name}) as date from {schema_name}.{table_name}) as temp where date = '1900-01-01'"
