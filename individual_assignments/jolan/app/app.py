import streamlit as st
import pandas as pd
import template as t

st.set_page_config(layout="wide")

# load the dataset with the books
df_content = pd.read_csv('../data/bbc_data_clean.csv', sep=';', index_col=False)
df_content['id'] = df_content['id'].astype(str)

# Load in cosine similarity matrix
cosine_similarity_matrix = pd.read_csv('../data/cosine_similarity.csv', sep=',', index_col=False)

# select a book to kickstart the interface
if 'id' not in st.session_state:
    st.session_state['id'] = '120'

df_item = df_content[df_content['id'] == st.session_state['id']]

# create a cover and info column to display the selected book
cover, info = st.columns([2, 3])

with cover:
    # display the image
    st.image(df_item['image'].iloc[0].format(recipe='464x261'))

with info:
    # display the book information
    st.title(df_item['title'].iloc[0])
    st.markdown(df_item['description'].iloc[0])
    st.caption(str(df_item['category'].iloc[0]) + ' | ' + df_item['topic'].iloc[0] + ' | ' + df_item['channel'].iloc[
        0] + ' | ' + df_item['release_date'].iloc[0])


# Now we will add recommendations
def get_cos_sim_recommendations(item_id, cos_sim_matrix):
    one_item_sim = cos_sim_matrix.loc[(cos_sim_matrix[item_id] < 1) & (
            cos_sim_matrix[item_id] != 0), item_id].sort_values(ascending=False)
    similar_recommendations = one_item_sim.to_frame().reset_index()
    similar_recommendations.columns = ['id', 'cos_sim']
    similar_recommendations['id'] = similar_recommendations['id'].astype(str)
    different_recommendations = one_item_sim[int((len(one_item_sim) * 0.5)):
                                             (int(len(one_item_sim) * 0.75))].to_frame().reset_index()
    different_recommendations.columns = ['id', 'cos_sim']
    different_recommendations['id'] = different_recommendations['id'].astype(str)

    return similar_recommendations, different_recommendations

if st.checkbox('Recommendation Control Mode'):
    randomness = st.slider(
        'Determine to what extent you want to be surprised by the content shown to you! '
        '1 unit on this slider equals 1 additional surprise! ',
        0, 10, 0, 1)
else:
    randomness = 0

st.caption('The similarity percentage that is shown underneath the recommendation indicates '
           'how similar the descriptions of the content are.')

# display the recommendations based upon similarity of synopses of the content
st.subheader('More Similar Content')
df_similar, df_diverse = get_cos_sim_recommendations(st.session_state['id'], cosine_similarity_matrix)
df_cos_sim = df_similar.merge(df_content, on='id')
df_cos_dif = df_diverse.merge(df_content, on='id')
# Only show 10 recommendations
df_cos_sim_recommendations = pd.concat([df_cos_sim.head(10 - randomness),
                                        df_cos_dif.sample(min(randomness, 10))])
t.recommendations(df_cos_sim_recommendations)


def get_header_topic(topic):
    return f'More {topic.capitalize()} Content'


# display the recommendations based upon category and the similarity of synopses of the content
# First create string for the header
st.subheader(get_header_topic(df_item['topic'].iloc[0]))
# Similarity for this book has already been calculated so re-use those dataframes
df_cos_sim_topic = df_cos_sim.loc[df_cos_sim['topic'] == df_item['topic'].iloc[0], :]
df_cos_dif_topic = df_cos_dif.loc[df_cos_dif['topic'] == df_item['topic'].iloc[0], :]
df_cos_sim_topic_recommendations = pd.concat([df_cos_sim_topic.head(10 - randomness),
                                              df_cos_dif_topic.sample(min(randomness, 10))])
t.recommendations(df_cos_sim_topic_recommendations)

# Display recommendations in different categories
st.subheader('More Content From Other categories')
# Similarity for this book has already been calculated so re-use those dataframes
df_cos_sim_topic = df_cos_sim.loc[df_cos_sim['topic'] != df_item['topic'].iloc[0], :]
df_cos_dif_topic = df_cos_dif.loc[df_cos_dif['topic'] != df_item['topic'].iloc[0], :]
df_cos_sim_topic_recommendations = pd.concat([df_cos_sim_topic.head(10 - randomness),
                                              df_cos_dif_topic.sample(min(randomness, 10))])
t.recommendations(df_cos_sim_topic_recommendations)
