import streamlit as st

from src.database.logics import PostgresConnector
from src.dataframe.display import read_data

def display_db_connection_menu():
    """
    --------------------
    Description
    --------------------
    -> display_db_connection_menu (function): Function that displays the menu for connecting to a database and triggers the database connection

    --------------------
    Parameters
    --------------------
    No parameter

    --------------------
    Pseudo-Code
    --------------------
    -> Display a header for the database connection menu "Database Connection Details".
    -> Display text inputs for users to insert required database connection information (host, database, port, username and password). \n
    -> Everytime the "Connect" button is clicked, the following events happen: 
    - Connect to database.
    - Refresh the page in order to re-render session_state container with updated values. 
    - If db_status of session_state is True, display a success message. 
    - Otherwise, display an error message.
    --------------------
    Returns
    --------------------
    -> (None)

    """
    st.header("Database Connection Details")

    st.text_input(
        'Username:',
        key='db_user',
    )
    
    st.text_input(
        'Password:',
        key='db_pass',
    )

    st.text_input(
        'Database Host:',
        key='db_host',
    )

    st.text_input(
        'Database Name:',
        key='db_name',
    )

    st.text_input(
        'Database Port:',
        key='db_port',
    )
    if st.button("Connect"):
        connect_db()
        st.experimental_rerun()

    if st.session_state.msg != None:
        if st.session_state.db_status:
            st.success(st.session_state.msg)
        else:
            st.error(st.session_state.msg)

def connect_db():
    """
    --------------------
    Description
    --------------------
    -> connect_db (function): Function that connects to a database and instantiate a PostgresConnector class accordingly

    --------------------
    Parameters
    --------------------
    No parameter

    --------------------
    Pseudo-Code
    --------------------
    -> Instantiate an instance of PostgresConnector class.
    -> Open the database connection.
    -> Set a value for msg of session_state.
    -> Set a value for db_status of session_state.
    -> Set a value for db of session_state.

    --------------------
    Returns
    --------------------
    -> (None)

    """
    postgresConnector = PostgresConnector(
        st.session_state.db_name, 
        st.session_state.db_user, 
        st.session_state.db_pass,
        st.session_state.db_host,  
        st.session_state.db_port
    )
    result = postgresConnector.open_connection()
    st.session_state.msg = result['msg']
    st.session_state.db_status = result['status']
    st.session_state.db = postgresConnector
    st.session_state.data = None

def display_table_selection():
    """
    --------------------
    Description
    --------------------
    -> display_table_selection (function): Function that displays the selection box for selecting the table to be analysed and triggers the loading of data (read_data())

    --------------------
    Parameters
    --------------------
    No parameter

    --------------------
    Pseudo-Code
    --------------------
    -> Get all schemas and their tables.
    -> Create a list of options which include all schema and their tables. 
    -> Display a selectbox. Whenever a table is selected, it trigger read_data() to get the table content. 

    --------------------
    Returns
    --------------------
    -> (None)

    """
    all_schemas_tables = st.session_state.db.list_tables()
    options = all_schemas_tables.apply(lambda row: str(row["table_schema"]) + "." + str(row["table_name"]), axis = 1)
    st.selectbox('Select a table name', options, key='schema_table_selected', on_change=select_schema_table)

def select_schema_table():
    split_schema_table = st.session_state.schema_table_selected.split('.')
    st.session_state.schema_selected = split_schema_table[0]
    st.session_state.table_selected = split_schema_table[1]
    read_data()
    
    