import streamlit as st
from random import random


# set episode session state
def select_item(id):
  st.session_state['id'] = id


def create_caption(title, cos_sim):
  return f'{title} \n \n{round((cos_sim * 100), 2)}% similar'


def tile_item(column, item):
  with column:
    st.button('📺', key=random(), on_click=select_item, args=(item['id'], ))
    st.image(item['image'].format(recipe='464x261'), use_column_width='always')
    st.caption(create_caption(item['title'], item['cos_sim']))


def recommendations(df):
  # check the number of items
  nbr_items = df.shape[0]

  if nbr_items != 0:    

    # create columns with the corresponding number of items
    columns = st.columns(nbr_items)

    # convert df rows to dict lists
    items = df.to_dict(orient='records')

    # apply tile_item to each column-item tuple (created with python 'zip')
    any(tile_item(x[0], x[1]) for x in zip(columns, items))

