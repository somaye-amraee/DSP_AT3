import os
import streamlit as st

def set_app_config():
    """
    --------------------
    Description
    --------------------
    -> set_app_config (function): Function that sets the configuration of the Streamlit app

    --------------------
    Parameters
    --------------------
    No parameter

    --------------------
    Pseudo-Code
    --------------------
    -> Set the page title, shown in the browser tab.
    -> Set the page icon, shown in the browser tab.
    -> Constrain page elements into a centered column of fixed width.
    -> Configure the menu that appears on the top-right side of this app.

    --------------------
    Returns
    --------------------
    -> (None)

    """
    st.set_page_config(
        page_title="DSP - AT3: Database explorer WebApp",
        page_icon="🧊",
        layout="centered",
        menu_items={
            'Get Help': 'mailto:phuongthao.nguyen-3@student.uts.edu.au',
            'Report a bug': "mailto:phuongthao.nguyen-3@student.uts.edu.au",
            'About': "# Database Exploration ! \n For any data-related project, data scientists need to have a good understanding of the input datasets. They usually perform exploratory data analysis (EDA) in order to get a deep understanding of the information provided, identifying issues and limitations. Therefore Team 20 collaborated to create a containerised web application in Python where users can perform some exploratory data analysis on selected tables."
    }
)

def set_session_state(key, value):
    """
    --------------------
    Description
    --------------------
    -> set_session_state (function): Function that saves a key-value pair to the Streamlit session state

    --------------------
    Parameters
    --------------------
    -> key (str): The session state's key.
    -> value (None): The default value of key.

    --------------------
    Pseudo-Code
    --------------------
    -> Only if the key does not exist in the session state, do we set default value for it. 
    -> If the key is "db_user", "db_pass", "db_host", "db_name", or "db_port", its default value is taken from docker-compose.yml's env configuration.
    -> Otherwise, the default value of the key is None. 

    --------------------
    Returns
    --------------------
    -> (None)

    """
    if key not in st.session_state:
        if key == 'db_user':
            st.session_state[key] = os.environ['POSTGRES_USER']
        elif key == 'db_pass':
            st.session_state[key] = os.environ['POSTGRES_PASSWORD']
        elif key == 'db_host':
            st.session_state[key] = os.environ['POSTGRES_HOST']
        elif key == 'db_name':
            st.session_state[key] = os.environ['POSTGRES_DB']
        elif key == 'db_port':
            st.session_state[key] = os.environ['POSTGRES_PORT']
        else:
            st.session_state[key] = value

def set_session_states(keys, value=None):
    """
    --------------------
    Description
    --------------------
    -> set_session_states (function): Function that saves a list of key-value pairs to the Streamlit session state using set_session_state() (default value: None)

    --------------------
    Parameters
    --------------------
    -> value (None): Default value of the session state's keys. 

    --------------------
    Pseudo-Code
    --------------------
    -> Iterate over all keys in session state and set default values to them. 

    --------------------
    Returns
    --------------------
    -> (None)

    """
    for key in keys:
        set_session_state(key, value)

def display_session_state():
    """
    --------------------
    Description
    --------------------
    -> display_session_state (function): Function that displays the current values of Streamlit session state

    --------------------
    Parameters
    --------------------
    No parameter

    --------------------
    Pseudo-Code
    --------------------
    -> Display the session state object.

    --------------------
    Returns
    --------------------
    -> (None)

    """
    st.write(st.session_state)
    



