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

USER = 'user'

# Activities
ACTIVITIES = 'activities'

def init_session_keys(users_activities):
    if ID not in st.session_state:
        st.session_state[ID] = random.randrange(0, 2200)
    if MODE not in st.session_state:
        st.session_state[MODE] = HOME
    if HISTORY not in st.session_state:
        st.session_state[HISTORY] = []
    if USER not in st.session_state:
        st.session_state[USER] = 0
    if ACTIVITIES not in st.session_state:
        st.session_state[ACTIVITIES] = users_activities



