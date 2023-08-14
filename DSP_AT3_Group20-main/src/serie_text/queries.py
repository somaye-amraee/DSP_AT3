def get_missing_query(schema_name, table_name, col_name):
    """
  
    --------------------
    Description
    --------------------
    -> get_missing_query (method): Function that returns the query used for computing the number of missing values of a column from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name - this is the name of the schema in the postgres database we are extracting
    table_name - the name of the table after selecting the specific schema name we analysing
    col_name - This is the column name with the table_name from the schem_name we selected, this will contain the name of the column attribute and its values.

    --------------------
    Pseudo-Code
    --------------------
    SELECT and COUNT the column name from schema name and table name
    WHERE the column name IS NULL; 

    --------------------
    Returns
    --------------------
    result of the count of null values appearing in the database

    """
    return f"SELECT COUNT({col_name}) FROM {schema_name}.{table_name} WHERE '{col_name}' IS NULL"

 
def get_mode_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_mode_query (method): Function that returns the query used for computing the mode value of a column from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name -  this is the name of the schema in the postgres database we are extracting
    table_name - the name of the table after selecting the specific schema name we analysing
    col_name - This is the column name with the table_name from the schem_name we selected, this will contain the name of the column attribute and its values.

    --------------------
    Pseudo-Code
    --------------------
    SELECT MODE() of the column name from schema name.table name


    --------------------
    Returns
    --------------------
    output of the number of frequent value appearing for the value

    """
    return f"SELECT MODE() WITHIN GROUP (ORDER BY {col_name}) from {schema_name}.{table_name}"
   # return f'"The mode value for {col_name} in {table_name} is "SELECT MODE() WITHIN GROUP (ORDER BY {col_name} from {schema_name}.{table_name}'

def get_alpha_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_alpha_query (method): Function that returns the query used for computing the number of times a column from a Postgres table has only alphabetical characters

    --------------------
    Parameters
    --------------------
    schema_name - this is the name of the schema in the postgres database we are extracting
    table_name -  the name of the table after selecting the specific schema name we analysing
    col_name - This is the column name with the table_name from the schem_name we selected, this will contain the name of the column attribute and its values.

    --------------------
    Pseudo-Code
    --------------------
    select and COUNT column name from schema name. table name
    WHERE column name is alphabetical letters disregarding whether it is upper or lower case letters

    --------------------
    Returns
    --------------------
    output the number of times alphabetical letters appear in the column name of the schema table.

    """

    return f"select count({col_name}) from {schema_name}.{table_name} where {col_name} ~* '[A-Z]'"
    #return f"The number of alphabetical characters only in {col_name} "select count({col_name}) from {schema_name}.{table_name} where {col_name} ~* '[A-Z]';"'