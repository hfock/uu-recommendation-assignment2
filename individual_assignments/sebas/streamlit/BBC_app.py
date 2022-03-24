import streamlit as st
import pandas as pd
import BBC_template as t
import numpy as np
from datetime import datetime

st.set_page_config(layout="wide")

# load the dataset with the books
df_BBC = pd.read_csv('../BBC_raw.csv', sep=';')
df_BBC = df_BBC.drop_duplicates(subset = ['title'])
df_BBC.dropna(subset = ["synops_long"], inplace = True)
df_BBC = df_BBC.reset_index()

with open('../similarity.npy', 'rb') as f:
    Similarity = np.load(f)
# define indices
indices = pd.Series(df_BBC.index, index = df_BBC['title']).drop_duplicates()

def get_recommendations(title, cosine, indices):
    # Get the index of the movie that matches the title
    idx = indices[title]
    # Get the pairwsie similarity scores
    sim_scores = list(enumerate(cosine[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse = True)
    # Get the scores for 10 most similar movies
    sim_scores = sim_scores[0:10]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return df_BBC['title'].iloc[movie_indices]

# select a book to kickstart the interface
if 'title' not in st.session_state:
  st.session_state['title'] = 'Planet Earth II'

show = df_BBC[df_BBC['title'] == st.session_state['title']]

# create a cover and info column to display the selected book
cover, info = st.columns([2, 3])

with cover:
  # display the image
  st.image(show['image'].iloc[0].format(recipe = "464x261"))

with info:
  # display the book information
  st.title(show['title'].iloc[0])
  st.markdown(show['synops_med'].iloc[0])

  if st.button('Like'):
    st.caption('Like Algorithm' + ' | ' + 'Personal Data')
    temp_ind = list(get_recommendations(show['title'].iloc[0], Similarity, indices).index)
    Similarity[:, temp_ind] += 0.1
  else:
    st.caption('TF-IDF Algorithm' + ' | ' + 'Non-Personal Data')
  st.caption(str(show['release_date'].iloc[0]) + ' | ' + show['channel'].iloc[0])



alpha = 0.2
alpha = st.select_slider('Escape Your Filter-Bubble by Moving the Slider to the Right',
                         options = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], value = 20) / 100
title = st.session_state['title']
selection = get_recommendations(title, Similarity, indices).index.values
RelDiversity = (1 - Similarity[list(selection)]).mean(axis = 0).round(2)
Quality = (1 - alpha) * Similarity + alpha * RelDiversity

st.subheader('Broaden Your Horizon!')
ind_qua = list(get_recommendations(title, Quality, indices).index)
df_recommendations = df_BBC.filter(items = ind_qua, axis = 0)
df_recommendations = df_recommendations.rename(columns = {"target": "title"})
t.recommendations(df_recommendations)

st.subheader('More Like This')
ind_sim = list(get_recommendations(title, Similarity, indices).index)
df_recommendations = df_BBC.filter(items = ind_sim, axis = 0)
df_recommendations = df_recommendations.rename(columns = {"target": "title"})
t.recommendations(df_recommendations)

st.subheader('What Do You Want to See?')
options = set(df_BBC.category)
options = st.multiselect('Filter on recent shows by categories', set(df_BBC.category))
df_BBC_filter = df_BBC[df_BBC.category.isin(options)]
format = "%Y"
df_BBC_filter["release_date"] = [datetime.strptime(dates[-4:], format) for dates in df_BBC_filter.release_date]
df_BBC_filter = df_BBC_filter.sort_values(by = ["release_date"], ascending = False)
df_recommendations = df_BBC_filter.head(10)
df_recommendations = df_recommendations.rename(columns = {"target": "title"})
t.recommendations(df_recommendations)

st.subheader('Why Shows are Related')
col1, col2 = st.columns(2)
show1 = col1.text_input('Show title', 'Eurovision Song Contest')
show2 = col2.text_input('Show title', 'Planet Earth II')
st.write(f"The description between {show1} and {show2} is {round(Similarity[indices[show1], indices[show2]]*100, 2)}% similar")