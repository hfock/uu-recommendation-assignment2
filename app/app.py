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

    df_adv = pd.read_csv(f'{c.DATA_PATH}bbc_data_adv.csv', index_col=0, delimiter=';')

    return df, df_cosine, df_users, df_adv


@st.cache(allow_output_mutation=True)
def load_muatable_data():
    with open(f'{c.DATA_PATH}activities.json') as json_file:
        users_activities = json.load(json_file)
    df_user_activity = pd.DataFrame(users_activities)

    user_movie_dict = extract_user_movie_dict(df_user_activity)

    with open(f'{c.DATA_PATH}collaborative_filtering/collab_filter_random_features.npy', 'rb') as f:
        numpy_colab_matrix = np.load(f)
    df_colab = pd.DataFrame(numpy_colab_matrix)

    return users_activities, user_movie_dict, df_colab


def init_page(df, df_cosine, df_colab, user_movie_dict, df_adv):
    if st.session_state[c.MODE] == c.HOME:
        sel_show = Show(entry_by_id(df, st.session_state[c.ID]))
        t.display_show(sel_show)

        recom_entries = r.most_similar(df, df_cosine, sel_show.index)
        t.recommendations(recom_entries, "Based on content's similarity")

        if st.session_state[c.USER] != 0:
            recom_entries_collab_content = r.most_similar_collab_content(df,
                                                                         df_cosine,
                                                                         df_colab,
                                                                         user_movie_dict,
                                                                         st.session_state[c.USER],
                                                                         sel_show.index)
            t.recommendations(recom_entries_collab_content, "Based on content's similarity and collaborative filtering")

            recom_entries_colab = r.most_similar_collab(df, df_colab, user_movie_dict, st.session_state[c.USER])
            t.recommendations(recom_entries_colab, "Based on collaborative filtering")

        if st.session_state[c.SIMPSON] == c.LISA or st.session_state[c.SIMPSON] == c.BART:
            st.session_state[c.GENRE] = st.selectbox('Genre', df['category'].sort_values().unique())
            recom_entries_genre = r.most_similar_by_genre(df, df_cosine, sel_show.index)
            t.recommendations(recom_entries_genre, "Based on content's similarity and genre")

        if st.session_state[c.SIMPSON] == c.LISA or st.session_state[c.SIMPSON] == c.MARGE:
            alpha = st.select_slider('Escape Your Filter-Bubble by Moving the Slider to the Right',
                                     options=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], value=20) / 100

            recom_entries_sim = r.most_similar(df, df_cosine, sel_show.index)
            rel_diversity = (1 - df_cosine.loc[recom_entries_sim.index]).mean(axis=0).round(2)
            quality = (1 - alpha) * df_cosine + alpha * rel_diversity

            ind_qua = r.most_similar(df, quality, sel_show.index)
            t.recommendations(ind_qua, 'Broaden Your Horizon!')

    elif st.session_state[c.MODE] == c.HISTORY:
        if st.session_state[c.HISTORY] or st.session_state[c.OLD_HISTORY]:
            history = st.session_state[c.HISTORY][::-1] + st.session_state[c.OLD_HISTORY][::-1]
            for entry_id in history:
                t.display_history(Show(entry_by_id(df, entry_id)))
        else:
            st.write('No History yet')
    elif st.session_state[c.MODE] == c.ADVANCED:
        t.advanced_view(df_adv)
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
    df, df_cosine, df_users, df_adv = load_data()
    users_activities, user_movie_dict, df_colab = load_muatable_data()

    # init session keys
    c.init_session_keys(users_activities)

    # init sidebar and authentication
    t.sidebar(df_users, user_movie_dict)

    init_page(df, df_cosine, df_colab, user_movie_dict, df_adv)
