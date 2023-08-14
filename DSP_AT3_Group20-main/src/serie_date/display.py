import streamlit as st

from src.serie_date.logics import DateColumn


def display_dates():
    """
    --------------------
    Description
    --------------------
    -> display_dates (function): Function that displays all the relevant information for every datetime column of a table

    --------------------
    Parameters
    --------------------
    None

    --------------------
    Pseudo-Code
    --------------------
    Extract dataset class in the session state and store it as a variable
    Call set_date_columns method to set the attributes values
    Create a variable to store the column names 
    If there is date col in the dataframe
    Set corresponding expanders and display the relevant information

    --------------------
    Returns
    --------------------
    => To be filled by student
    -> (type): description

    """
    data = st.session_state.data
    data.set_date_columns()
    date_cols = data.date_cols

    if date_cols is not None:
        for col in date_cols:
            with st.expander(col, expanded=False):
                display_date(col, None)

def display_date(col_name, i):
    """
    --------------------
    Description
    --------------------
    -> display_date (function): Function that instantiates a DateColumn class from a dataframe column and displays all the relevant information for a single datetime column of a table

    --------------------
    Parameters
    --------------------
    col_name(str): column name to create the DateColumn class
    i(str): not used 

    --------------------
    Pseudo-Code
    --------------------
    Initiate a DateColumn class with provided parameters in the session state and store it as a new variable
    Call set_data method of the DateColumn class
    Call get_summary_df of the DateColumn class and show it as a static table in the streamlit app
    Set a bar chart title
    Show the barchart which is created using altair package in the streamlit app
    Set a title for the following dataframe
    Call frequent method of the DateColumn class and show it in the streamlit app

    --------------------
    Returns
    --------------------
    None

    """
    date_column = DateColumn(st.session_state.schema_selected, st.session_state.table_selected, col_name, st.session_state.db, st.session_state.data.df[col_name])
    date_column.set_data()
    st.table(date_column.get_summary_df())
    st.text('Bar Chart')
    st.altair_chart(date_column.barchart)
    st.text('Most Frequent Values')
    st.dataframe(date_column.frequent)