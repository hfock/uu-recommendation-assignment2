import constant as c
import streamlit as st
import pandas as pd

import random


def init_session_keys():
    if c.ID not in st.session_state:
        st.session_state[c.ID] = random.randrange(0, 2200)
    if c.MODE not in st.session_state:
        st.session_state[c.MODE] = c.EXPLORE
    if c.HISTORY not in st.session_state:
        st.session_state[c.HISTORY] = []
    if c.TRANSPARENCY not in st.session_state:
        st.session_state[c.TRANSPARENCY] = False
    if c.PRIVACY not in st.session_state:
        st.session_state[c.PRIVACY] = False
    if c.GENRE_FILTER not in st.session_state:
        st.session_state[c.GENRE_FILTER] = False
    if c.GENRE not in st.session_state:
        st.session_state[c.GENRE] = 'Arts'
    if c.DIVERSITY not in st.session_state:
        st.session_state[c.DIVERSITY] = True


# latin-1
def load_csv(csv_file_path, delimiter=';', index_col=None, low_memory=False):
    return pd.read_csv(csv_file_path,
                       delimiter=delimiter,
                       index_col=index_col,
                       low_memory=low_memory)


def save_csv(df, csv_file_path, index=False):
    df.to_csv(csv_file_path, index=index)
