import streamlit as st
from src.dataframe.logics import Dataset


def read_data():
    """
    --------------------
    Description
    --------------------
    -> read_data (function): Function that loads the content of the Postgres table selected, extract its schema information and instantiate a Dataset class accordingly

    --------------------
    Parameters
    --------------------
    None

    --------------------
    Pseudo-Code
    --------------------
    create variables to store session_state value 
    create dataset class and store in session_state

    --------------------
    Returns
    --------------------
    None
    """
    postgresConnector = st.session_state.db

    schema_name = st.session_state.schema_selected

    table_name = st.session_state.table_selected

    table_content = postgresConnector.load_table(schema_name, table_name)

    st.session_state.data = Dataset(schema_name, table_name, postgresConnector, table_content)
      

def display_overall():
    """
    --------------------
    Description
    --------------------
    -> display_overall (function): Function that displays all the information on the Overall section of the streamlit app

    --------------------
    Parameters
    --------------------
    None

    --------------------
    Pseudo-Code
    --------------------
    call set_data method of dataset class
    create title for overall table 
    call get_summary_df method of dataset class
    create title for overall dataframe

    --------------------
    Returns
    --------------------
    None

    """
    st.session_state.data.set_data()
    st.text('Overall Information')
    st.table(st.session_state.data.get_summary_df())
    st.text('Table Schema:')
    st.dataframe(st.session_state.db.get_table_schema(st.session_state.schema_selected, st.session_state.table_selected))

def display_dataframes():
    """
    --------------------
    Description
    --------------------
    -> display_dataframes (function): Function that displays all the information on the Explore section of the streamlit app

    --------------------
    Parameters
    --------------------
    None

    --------------------
    Pseudo-Code
    --------------------
    create title for explore part of the app 
    create slider 
    create radio 
    if statement to call relevant method in the dataset class

    --------------------
    Returns
    --------------------
    None

    """
    st.text('Explore Dataframe')

    n = st.slider('Select the number of rows to be displayed',5, 50, 5)
    method = st.radio('Exploration Method', ('Head', 'Tail', 'Sample'))
    if method == 'Head':
        st.write('Top Rows of Selected Table')
        st.dataframe(st.session_state.data.get_head(n))
    elif method == 'Tail':
        st.write('Bottom Rows of Selected Table')
        st.dataframe(st.session_state.data.get_tail(n))
    else:
        st.write('Random Sample Rows of Selected Table')
        st.dataframe(st.session_state.data.get_sample(n))
    
    

