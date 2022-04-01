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
    df = pd.read_csv(f'{c.DATA_PATH}bbc_small.csv', index_col=0, delimiter=';')
    df_cosine = pd.read_csv(f'{c.DATA_PATH}bbc_cosine_small.csv', index_col=0, delimiter=';')

    df_users = pd.read_json(f'{c.DATA_PATH}users.json')

    return df, df_cosine, df_users


@st.cache(allow_output_mutation=True)
def load_muatable_data():
    with open(f'{c.DATA_PATH}activities.json') as json_file:
        users_activities = json.load(json_file)
    df_user_activity = pd.DataFrame(users_activities)

    user_movie_dict = extract_user_movie_dict(df_user_activity)

    with open('../data/collaborative_filtering/collab_filter_random_features.npy', 'rb') as f:
        numpy_colab_matrix = np.load(f)
    df_colab = pd.DataFrame(numpy_colab_matrix)

    return users_activities, user_movie_dict, df_colab


def init_page(df, df_cosine, df_colab, user_movie_dict):
    if st.session_state[c.MODE] == c.HOME:
        sel_show = Show(entry_by_id(df, st.session_state[c.ID]))
        t.display_show(sel_show)

        recom_entries = r.most_similar(df, df_cosine, sel_show.index)
        t.recommendations(recom_entries, "Based on content's similarity")

        if st.session_state[c.USER] != 0:
            recom_entries_colab = r.most_similar_collab(df, df_colab, user_movie_dict, st.session_state[c.USER])
            t.recommendations(recom_entries_colab, "Based on collaborative filtering")


    elif st.session_state[c.MODE] == c.HISTORY:
        if st.session_state[c.HISTORY] or st.session_state[c.OLD_HISTORY]:
            history = st.session_state[c.HISTORY][::-1] + st.session_state[c.OLD_HISTORY][::-1]
            for entry_id in history:
                t.display_history(Show(entry_by_id(df, entry_id)))
        else:
            st.write('No History yet')

    else:
        st.session_state[c.MODE] = c.HOME


def entry_by_id(df_input: pd.DataFrame, id_input: int):
    return df_input[df_input[c.ID] == id_input].iloc[0]


def extract_user_movie_dict(df_user_activity):
    user_list = df_user_activity.user_id.unique()
    user_movie_dict = {}
    for user_id in user_list:
        user_entries = df_user_activity[df_user_activity['user_id'] == user_id]
        user_movie_dict[user_id - 1] = user_entries.content_id.unique()
    return user_movie_dict


if __name__ == '__main__':
    st.set_page_config(layout="wide")

    # load data
    df, df_cosine, df_users = load_data()
    users_activities, user_movie_dict, df_colab = load_muatable_data()

    # init session keys
    c.init_session_keys(users_activities)

    # init sidebar and authentication
    t.sidebar(df_users, user_movie_dict)

    init_page(df, df_cosine, df_colab, user_movie_dict)
