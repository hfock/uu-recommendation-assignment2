# Import
import numpy as np
import pandas as pd
import streamlit as st
import json

import constant as c
import template as t
import recommendations as r

from show import Show


@st.cache
def load_data():
    bbc_dataframe = pd.read_csv(f'{c.DATA_PATH}bbc_data_slim.csv', delimiter=',')
    bbc_cosin_sim = pd.read_csv(f'{c.DATA_PATH}cosine_similarity.csv', index_col=0, delimiter=';')

    with open(f'{c.DATA_PATH}similarity.npy', 'rb') as f:
        similarity = np.load(f)

    df_users = pd.read_json(f'{c.DATA_PATH}users.json')

    return bbc_dataframe, bbc_cosin_sim, similarity, df_users

@st.cache(allow_output_mutation=True)
def load_muatable_data():
    with open(f'{c.DATA_PATH}activities.json') as json_file:
        users_activities = json.load(json_file)
    return users_activities


def init_page():

    if st.session_state[c.MODE] == c.HOME:
        sel_show = Show(entry_by_id(df, st.session_state[c.ID]))
        t.display_show(sel_show)

        recom_entries = df.iloc[r.sim_title(df_cosin, st.session_state[c.ID]), :]
        t.recommendations(recom_entries, "Based on content's similarity")

    elif st.session_state[c.MODE] == c.HISTORY:
        if st.session_state[c.HISTORY]:
            print(st.session_state[c.HISTORY])
            for entry_id in st.session_state[c.HISTORY][::-1]:
                t.display_history(Show(entry_by_id(df, entry_id)))
        else:
            st.write('No History yet')

    else:
        st.session_state[c.MODE] = c.HOME


def entry_by_id(df_input: pd.DataFrame, id_input: int):
    return df_input[df_input[c.ID] == id_input].iloc[0]


if __name__ == '__main__':
    st.set_page_config(layout="wide")

    # load data
    df, df_cosin, np_sim, df_users = load_data()
    users_activities = load_muatable_data()

    # init session keys
    c.init_session_keys(users_activities)

    # init sidebar and authentication
    t.sidebar(df_users)

    init_page()



