import constant as c
import numpy as np
import streamlit as st
import pandas as pd


def sim_title(df_cosin_similarity, index: int):
    recoms = df_cosin_similarity.loc[index].sort_values(ascending=False).index.tolist()[1:c.RECOM_COUNT]
    return list(map(int, recoms))


def cosine_recommendations(np_sim, index):
    # Get the pairwsie similarity scores
    sim_scores = list(enumerate(np_sim[index]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores for the defined amount of recoms most similar movies
    sim_scores = sim_scores[1:c.RECOM_COUNT+1]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    return movie_indices


def most_similar_nparray(np_cosine, index):
    return np.sort(np_cosine[index, :c.RECOM_COUNT])[::-1]


def most_similar(df, df_cosine, index):
    recom_indices = df_cosine.loc[index].sort_values(ascending=False).index.tolist()[1:c.RECOM_COUNT]

    # Cast list to int
    recom_indices = list(map(int, recom_indices))
    recom_entries = df.loc[recom_indices, :]

    return recom_entries


def most_similar_collab(df, df_colab, user_movie_dict, logged_in_user):
    for user, movie in user_movie_dict.items():
        df_colab.loc[user, movie] = 0

    recom_indices = df_colab.T[logged_in_user - 1].sort_values(ascending=False).index.tolist()[1:c.RECOM_COUNT]
    recom_entries = df.loc[recom_indices, :]
    return recom_entries


def most_similar_by_genre(df, df_cosine, index):
    # Getting all the items that have the specific genre
    fitting_genre = df[df['category'] == st.session_state[c.GENRE]]
    # Get only the column of the wanted index
    cos_col_index = df_cosine.loc[index]
    # Remove all entries that are not within the selected genre
    genre_selected = cos_col_index.iloc[fitting_genre.index]
    # Sort them ascending and take the top x values
    recom_indices = genre_selected.sort_values(ascending=False).index.tolist()[1:c.RECOM_COUNT]
    recom_entries = df.loc[list(map(int, recom_indices)), :]
    return recom_entries


def most_similar_collab_content(df, df_cosine, df_colab, user_movie_dict, user_id, index):
    # for user, movie in user_movie_dict.items():
    #     df_colab.loc[user, movie] = 0
    colab_np = np.array(df_cosine.loc[index].tolist())

    cosin_np = np.array(df_colab.loc[user_id - 1].tolist())
    hybrid_solution = np.multiply(cosin_np, colab_np)
    recom_indices = pd.DataFrame(hybrid_solution).sort_values(by=0, ascending=False).index.tolist()[1:c.RECOM_COUNT]
    recom_entries = df.loc[list(map(int, recom_indices)), :]
    return recom_entries