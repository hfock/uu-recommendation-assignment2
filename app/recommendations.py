import constant as c


def sim_title(df_cosin_similarity, index: int):
    recoms = df_cosin_similarity.loc[index].sort_values(ascending=False).index.tolist()[1:c.RECOM_COUNT]
    return list(map(int, recoms))