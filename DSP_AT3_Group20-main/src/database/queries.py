
def get_tables_list_query():
	"""
    --------------------
    Description
    --------------------
    -> get_tables_list_query (method): Function that returns the query used for extracting the list of tables from a Postgres table

    --------------------
    Parameters
    --------------------
    No parameter

    --------------------
    Pseudo-Code
    --------------------
    -> Return the query that extracts the list of tables from a Postgres database, excluding information_schema and pg_catalog schemas.
    --------------------
    Returns
    --------------------
    -> (str): The query that extracts the list of tables from a Postgres database, excluding information_schema and pg_catalog schemas.

    """
	return "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema not in ('information_schema', 'pg_catalog')"

def get_table_data_query(schema_name, table_name):
	"""
    --------------------
    Description
    --------------------
    -> get_table_data_query (method): Function that returns the query used for extracting the content of a Postgres table

    --------------------
    Parameters
    --------------------
    -> schema_name (str): Name of the selected schema.
    -> table_name  (str): Name of the selected table.

    --------------------
    Pseudo-Code
    --------------------
    -> Return the query that extracts the content of the selected table.

    --------------------
    Returns
    --------------------
    -> (str): The query that extracts the content of the selected table.

    """
	return f'SELECT * FROM {schema_name}.{table_name}'

def get_table_schema_query(schema_name, table_name):
	"""
    --------------------
    Description
    --------------------
    -> get_table_schema_query (method): Function that returns the query used for extracting the list of columns from a Postgres table and their information

    --------------------
    Parameters
    --------------------
    -> schema_name (str): Name of the selected schema.
    -> table_name  (str): Name of the selected table.

    --------------------
    Pseudo-Code
    --------------------
    -> Return the query that extracts the list of columns from the selected table and their information.

    --------------------
    Returns
    --------------------
    -> (str): The query that extracts the list of columns from the selected table and their information.

    """
	return f"SELECT * FROM information_schema.columns WHERE table_schema = '{schema_name}' and table_name = '{table_name}'"
