# Import
import pandas as pd
import streamlit as st
import constant as c

# import own files
import model as md
import view as vw
import random

from CurrentShow import CurShow


@st.cache
def load_data():
    bbc_dataframe = pd.read_csv(f'{c.DATA_BBC}bbc_data_slim.csv', delimiter=',')
    bbc_table_view_dataframe = pd.read_csv(f'{c.DATA_BBC}bbc_data_adv.csv', index_col=0, delimiter=';')
    bbc_cosin_sim = pd.read_csv(f'{c.DATA_BBC}cosine_similarity.csv', index_col=0, delimiter=';')

    return bbc_dataframe, bbc_table_view_dataframe, bbc_cosin_sim


def entry_by_id(df_input: pd.DataFrame, id_input: int):
    return df_input[df_input[c.ID] == id_input].iloc[0]


def page_load():
    if st.session_state[c.MODE] == c.EXPLORE:
        cur_show = CurShow(entry_by_id(df, st.session_state[c.ID]))
        vw.display_selected_item(cur_show)

        number_of_items = 6
        recom_entries = df.iloc[sim_title(df_cosin, st.session_state[c.ID], number_of_items), :]
        vw.recommendations(recom_entries,
                           "Recommendations based on the current content's similarity")

        if st.session_state[c.DIVERSITY]:
            recom_on_artifical = df.iloc[sim_title_artifical_cluster(df, st.session_state[c.ID], number_of_items), :]
            vw.recommendations(recom_on_artifical,
                               "Recommendations based on current content's domain of interest")

        if st.session_state[c.GENRE_FILTER]:
            recom_on_genre = df.iloc[sim_title_by_genre(df, df_cosin, st.session_state[c.ID], number_of_items)]
            vw.recommendations(recom_on_genre,
                               'Recommendations based on the current content and selected genre')

        if not st.session_state[c.PRIVACY]:
            hist_recom_entries = df.iloc[sim_title_by_many(df_cosin, st.session_state[c.HISTORY], number_of_items)]
            vw.recommendations(hist_recom_entries,
                               'Recommendations based on your history')

    elif st.session_state[c.MODE] == c.ADVANCED:
        vw.exploration(df_adv)

    elif st.session_state[c.MODE] == c.HISTORY:
        if st.session_state[c.HISTORY]:
            for entry_id in st.session_state[c.HISTORY][::-1]:
                vw.display_history(CurShow(entry_by_id(df, entry_id)))
        else:
            st.write('No History yet')
    else:
        st.session_state[c.MODE] = c.EXPLORE


def sim_title(df_cosin_similarity, index: int, number_of_recom):
    recoms = df_cosin_similarity.loc[index].sort_values(ascending=False).index.tolist()[1:number_of_recom]
    return list(map(int, recoms))


def sim_title_artifical_cluster(df_bbc, index: int, number_of_recom):
    artifical_cat = df_bbc[df_bbc['index'] == index]['adv_category'].iloc[0]
    recoms = df_bbc[df_bbc['adv_category'] == artifical_cat]

    list_of_available_items = recoms.index.tolist()
    print(list_of_available_items)
    if number_of_recom > len(list_of_available_items):
        number_of_recom = len(list_of_available_items)
    recoms = random.sample(list_of_available_items, number_of_recom)
    return list(map(int, recoms))


def sim_title_by_many(df_cosin_similarity, indices: list, number_of_recom):
    combined = df_cosin_similarity.iloc[:, indices]
    combined['combined'] = combined.mean(axis=1)
    combined = combined.drop(st.session_state[c.HISTORY], axis=0)
    recoms = combined['combined'].sort_values(ascending=False).index.tolist()[1:number_of_recom]
    return list(map(int, recoms))


def sim_title_by_genre(df, df_cosin_similarity, index, number_of_recom):
    # Getting all the items that have the specific genre
    fitting_genre = df[df['category'] == st.session_state[c.GENRE]]
    # Get only the column of the wanted index
    cos_col_index = df_cosin_similarity.loc[index]
    # Remove all entries that are not within the selected genre
    genre_selected = cos_col_index.iloc[fitting_genre.index]
    # Sort them ascending and take the top x values
    recoms = genre_selected.sort_values(ascending=False).index.tolist()[1:number_of_recom]
    return list(map(int, recoms))


if __name__ == '__main__':
    st.set_page_config(layout="wide")

    # init session keys
    md.init_session_keys()

    # load data
    df, df_adv, df_cosin = load_data()

    vw.sidebar(df)

    page_load()
