from numpy import character


def get_numeric_tables_query(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    -> get_numeric_tables_query (method): Function that returns the query used for extracting the list of numeric columns from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str): The schema name of the selected table in the target database 
    table_name(str): The table name of the selected table in the target database

    --------------------
    Pseudo-Code
    --------------------
    SQL query to select the numeric column names

    --------------------
    Returns
    --------------------
    A query string which can extract the numeric column names in the database

    """
    return f"select column_name from information_schema.columns as col where col.data_type in ('smallint', 'integer', 'bigint','decimal', 'numeric', 'real', 'double precision','smallserial', 'serial', 'bigserial', 'money') and col.table_schema not in ('information_schema', 'pg_catalog') and col.table_schema = '{schema_name}' and col.table_name = '{table_name}'"

def get_text_tables_query(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    -> get_text_tables_query (method): Function that returns the query used for extracting the list of text columns from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str): The schema name of the selected table in the target database
    table_name(str): The table name of the selected table in the target database 

    --------------------
    Pseudo-Code
    --------------------
    SQL query to select the text column names

    --------------------
    Returns
    --------------------
    A query string which can extract the text column names in the database

    """
    return f"select column_name from information_schema.columns as col where col.data_type in ('char', 'varchar', 'text','character varying','character') and col.table_schema not in ('information_schema', 'pg_catalog') and col.table_schema = '{schema_name}' and col.table_name = '{table_name}'"
    # character_types = ('character varying','varchar','char','text','character')
    # text_columns = (f"select column_name from information_schema.columns as col WHERE col.table_schema = '{schema_name}' and col.table_schema not in ('information_schema', 'pg_catalog') and col.table_name = '{table_name}' and col.data_type = {character_types}::character varying")
    # return text_columns

def get_date_tables_query(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    -> get_date_tables_query (method): Function that returns the query used for extracting the list of datetime columns from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str): The schema name of the selected table in the target database
    table_name(str): The table name of the selected table in the target database 

    --------------------
    Pseudo-Code
    --------------------
    SQL query to select the date column names 

    --------------------
    Returns
    --------------------
    A query string which can extract the date column names in the database

    """
    return f"select column_name from information_schema.columns as col where col.data_type in ('date', 'time', 'timestamp', 'timestampz', 'timetz') and col.table_schema not in ('information_schema', 'pg_catalog') and col.table_schema = '{schema_name}' and col.table_name = '{table_name}'"

def get_primary_key(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    -> get_primary_key (method): Function that returns the query used for extracting the list of primary key columns from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str): The schema name of the selected table in the target database 
    table_name(str): The table name of the selected table in the target database 

    --------------------
    Pseudo-Code
    --------------------
    SQL query to select the primary key column names

    --------------------
    Returns
    --------------------
    A query string which can extract the primary keys in the selected table
    """
    return f"select c.column_name from information_schema.table_constraints t left join information_schema.constraint_column_usage c on c.constraint_name = t.constraint_name where t.table_schema = '{schema_name}' and t.constraint_type = 'PRIMARY KEY' and t.table_name = '{table_name}'"