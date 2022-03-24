import constant as c
import streamlit as st

import random

from show import Show
import authenticate as auth


def sidebar(df_users):
    with st.sidebar:
        auth.authenticate(df_users)

        st.session_state[c.MODE] = st.sidebar.radio('Go To', [c.HOME, c.HISTORY])


def display_history(show: Show):
    left, right = st.columns([2, 2])

    with left:
        st.image(show.img)
    with right:
        st.caption(show.desc)
        st.caption(f'Category: {show.category}')
        st.button('🕶', key=random.random(), on_click=select_show, args=(show.index, False,))


def display_show(cur_show: Show):
    st.title(cur_show.title)
    left, middle, right = st.columns([1, 3,  1])
    with middle:
        st.image(cur_show.img)
    st.caption(cur_show.desc)
    st.caption(f'Category: {cur_show.category}')


def recommendations(df, text='Enter a Text for the header of the recommendation'):
    if text:
        st.markdown(f'#### {text}')

    # check the number of items
    nbr_items = df.shape[0]

    if nbr_items != 0:
        # create columns with the corresponding number of items
        columns = st.columns(nbr_items)

        # convert df rows to dict lists
        items = df.to_dict(orient='records')
        # apply tile_item to each column-item tuple (created with python 'zip')
        any(tile_item(x[0], x[1]) for x in zip(columns, items))


def tile_item(column, item):
    with column:
        st.button('📺', key=random.random(), on_click=select_show, args=(item['index'],))
        st.image(item['img'], use_column_width='always')
        st.markdown(f'''
        *{item["category"]}*
        ##### {item["title"]}
        ''')


def select_show(id, history=True):
    if history:
        record_history(id)
    st.session_state[c.ID] = id


def record_history(id):
    st.session_state[c.HISTORY].append(id)