import streamlit as st
import random

DATA_PATH = './../data/'

ID = 'index'

# Count of shown recommendations per list
RECOM_COUNT = 8

# Values for switching page view.
MODE = 'mode'

HOME = 'Home'
HISTORY = 'History'

# Authentication values
AUTH_STATUS = 'authentication_status'


def init_session_keys():
    if ID not in st.session_state:
        st.session_state[ID] = random.randrange(0, 2200)
    if MODE not in st.session_state:
        st.session_state[MODE] = HOME
    if HISTORY not in st.session_state:
        st.session_state[HISTORY] = []


