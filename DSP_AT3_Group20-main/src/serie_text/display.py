import streamlit as st

from src.serie_text.logics import TextColumn

def display_texts():
    """
    --------------------
    Description
    --------------------
    -> display_texts (function): Function that displays all the relevant information for every text column of a table

    --------------------
    Parameters
    --------------------
    => To be filled by student
    -> name (type): description

    --------------------
    Pseudo-Code
    --------------------
    => To be filled by student
    -> pseudo-code

    --------------------
    Returns
    --------------------
    => To be filled by student
    -> (type): description

    """
    
    text = st.session_state.data
    text.set_text_columns()
    text_cols = text.text_cols

    if text_cols is not None:
        for col in text_cols:
            with st.expander(col, expanded=False):
                display_text(col, None) 



# def get_text_tables_query(schema_name, table_name):
#   return f"select column_name from information_schema.columns as col where col.data_type in ('char', 'varchar', 'text') and col.table_schema not in ('information_schema', 'pg_catalog') and col.table_schema = '{schema_name}' and col.table_name = '{table_name}'"



def display_text(col_name, i):
    """
    --------------------
    Description
    --------------------
    -> display_text (function): Function that instantiates a TextColumn class from a dataframe column and displays all the relevant information for a single text column of a table

    --------------------
    Parameters
    --------------------
    => To be filled by student
    -> name (type): description

    --------------------
    Pseudo-Code
    --------------------
    => To be filled by student
    -> pseudo-code

    --------------------
    Returns
    --------------------
    => To be filled by student
    -> (type): description

    """
    text_column = TextColumn(st.session_state.schema_selected, st.session_state.table_selected, col_name, st.session_state.db, st.session_state.data.df[col_name])
    text_column.set_data()
    st.table(text_column.get_summary_df())
    st.text('Bar Chart')
    st.altair_chart(text_column.barchart)
    st.text('Most Frequent Values')
    st.dataframe(text_column.frequent)


