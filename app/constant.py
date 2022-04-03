import streamlit as st
import random
from enum import Enum

DATA_PATH = './../data/'
DATA_PATH_SIMPSONS = '../data/simpson_faces/'

ID = 'index'

# Count of shown recommendations per list
RECOM_COUNT = 8

# Values for switching page view.
MODE = 'mode'

HOME = 'Home'
HISTORY = 'History'
ADVANCED = 'Advanced'
OLD_HISTORY = 'Old History'

# Authentication values
AUTH_STATUS = 'authentication_status'

USER = 'user'

# Activities
ACTIVITIES = 'activities'

WATCHED = 'watched'

# DF Attributes
DF_DESCRIPTION= 'description'
DF_IMAGE_PREVIEW = 'image_l'
DF_IMAGE_LARGE = 'image_xl'
DF_CATEGORY = 'category'

# Simpson
SIMPSON = 'simpson'
HOMER = 'homer'
MARGE = 'marge'
LISA = 'lisa'
BART = 'bart'

# Genre
GENRE = 'genre'

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
    if OLD_HISTORY not in st.session_state:
        st.session_state[OLD_HISTORY] = []
    if SIMPSON not in st.session_state:
        st.session_state[SIMPSON] = HOMER
    if GENRE not in st.session_state:
        st.session_state[GENRE] = 'Comedy'