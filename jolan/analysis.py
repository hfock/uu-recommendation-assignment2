import pandas as pd
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load in English nlp object
nlp = spacy.load("en_core_web_sm")

# Load in the data
df = pd.read_csv('0_individual_assignment/data/bbc_data.csv', sep=';', index_col=False)

# Drop duplicate rows as some shows have multiple episodes in dataset
df = df.drop_duplicates(subset='title')

# Put the release date in same format
df['release_date'] = pd.to_datetime(df['release_date']).dt.strftime('%m/%d/%Y')

# Remove trailing newline and spacing characters from string columns
df = df.replace(r'\n',' ', regex=True)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Check whether there are any missing values in the columns
df.isnull().sum()

# Unfortunately not all records have long synopsis available
# If long synops is missing attempt to fill this with medium synops
# or otherwise use short synops as these have no missings
for index, row in df.iterrows():
    if pd.isna(row['synops_long']):
        if pd.isna(row['synops_med']):
            df.loc[index, 'synops_long'] = row.loc['synops_small']
        else:
            df.loc[index, 'synops_long'] = row.loc['synops_med']

# Id column and index now has missing values so change that before saving to csv
df.reset_index(drop=True, inplace=True)
df['id'] = df.index

# Write this cleaned df to csv to use in app
df.to_csv('0_individual_assignment/data/bbc_data_clean.csv', sep=';', index=False)

# Lower case the category
df['category'] = df['category'].str.lower()

# Fill na at category to prevent errors use . as this will be filtered out later
df['category'].fillna('.', inplace=True)

# To increase the recommendation accuracy add the category, channel, release date and topic at the end of the text
# Loop over df and check whether category and topic are same if not add both
df['synops_extended'] = np.nan
for index, row in df.iterrows():
        if row['category'] == row['topic']:
            df.loc[index, 'synops_extended'] = row['synops_long'] + ' ' + row['channel'] + ' ' + \
                                               ' ' + row['category']
        else:
            df.loc[index, 'synops_extended'] = row['synops_long'] + ' ' + row['channel'] + ' ' + \
                                               ' ' + row['category'] + ' ' + row['topic']

# Transform to lowercase and delete punctuation
def clean_column_of_text(column_of_text):
    # Load in English nlp object
    nlp = spacy.load("en_core_web_sm")

    # Column to list
    list = column_of_text.astype(str).to_list()

    # Preprocess list to nlp item
    processed = [text for text in nlp.pipe(list, disable=['ner', 'parser'])]

    # Lemmatize, lowercase, and delete stopwords and punctuation
    tokens = [[token.lemma_.lower() for token in text if not token.is_punct
                 and not token.is_stop] for text in processed]

    # Return processed tokens that are put back together in one string
    return [' '.join(token) for token in tokens]


df['text'] = clean_column_of_text(df['synops_long'])


# Create tfidf representation
tfidf_vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(df['text'])

# Calculate the cosine similarities
cosine_similarity = cosine_similarity(tfidf, tfidf)

# Write the cosine similarity matrix to a csv so we can use it in recommendations
pd.DataFrame(cosine_similarity).to_csv('0_individual_assignment/data/cosine_similarity.csv', index=False)

# Read in the data
cos_sim_matrix = pd.read_csv('0_individual_assignment/data/cosine_similarity.csv')

# Code to select one row and select the top 10 most similar items and a selection of 10 random items in 25-50 quantile
item_id = cos_sim_matrix.columns[0]
one_item_sim = cos_sim_matrix.loc[(cos_sim_matrix[item_id] < 1) & (
        cos_sim_matrix[item_id] != 0), item_id].sort_values(ascending=False)
top_10_sim = one_item_sim.head(10)
other_sim = one_item_sim[int((len(one_item_sim) * 0.5)): (int(len(one_item_sim) * 0.75))].sample(n=10)
