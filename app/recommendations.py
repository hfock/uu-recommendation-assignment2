import constant as c
import numpy as np


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

def most_similar(df, df_cosin, index):
    recom_indices = df_cosin.loc[index].sort_values(ascending=False).index.tolist()[1:c.RECOM_COUNT]

    # Cast list to int
    recom_indices = list(map(int, recom_indices))
    recom_entries = df.loc[recom_indices, :]

    return recom_entries