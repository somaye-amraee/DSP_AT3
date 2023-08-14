import streamlit as st

from src.serie_numeric.logics import NumericColumn

def display_numerics():
    """
    --------------------
    Description
    --------------------
    -> display_numerics (function): Function that displays all the relevant information for every numerical column of a table

    --------------------
    Parameters
    --------------------
    None

    --------------------
    Pseudo-Code
    --------------------
    Extract dataset class in the session state and store it as a variable
    Call set_numeric_columns method to set the attributes values
    Create a variable to store the column names 
    If there is num col in the dataframe
    Set corresponding expanders and display the relevant information

    --------------------
    Returns
    --------------------
    => To be filled by student
    -> (type): description

    """
    numeric = st.session_state.data
    numeric.set_numeric_columns()
    num_cols = numeric.num_cols

    if num_cols is not None:
        for col in num_cols:
            with st.expander(col, expanded=False):
                display_numeric(col, None)

def display_numeric(col_name, i):
    """
    --------------------
    Description
    --------------------
    -> display_numeric (function): Function that instantiates a NumericColumn class from a dataframe column and displays all the relevant information for a single numerical column of a table

    --------------------
    Parameters
    --------------------
    col_name(str): column name to create the DateColumn class
    i(str): not used 

    --------------------
    Pseudo-Code
    --------------------
    Initiate a NumericColumn class with provided parameters in the session state and store it as a new variable
    Call set_data method of the numeric_column class
    Call get_summary_df of the numeric_column class and show it as a static table in the streamlit app
    Set a bar chart title
    Show the barchart which is created using altair package in the streamlit app
    Set a title for the following dataframe
    Call frequent method of the NumericColumn class and show it in the streamlit app

    --------------------
    Returns
    --------------------
    None

    """
    numeric_column = NumericColumn(st.session_state.schema_selected, st.session_state.table_selected, col_name, st.session_state.db, st.session_state.data.df[col_name])
    numeric_column.set_data()
    st.table(numeric_column.get_summary_df())
    st.text('Bar Chart')
    st.altair_chart(numeric_column.histogram)
    st.text('Most Frequent Values')
    st.dataframe(numeric_column.frequent)