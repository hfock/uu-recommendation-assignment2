import constant as c
import streamlit as st

import random

from show import Show
import authenticate as auth
import user_interaction_collector as uic


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


def display_show(show: Show):
    st.title(show.title)
    left, right, super_right = st.columns([2,  2, 1])
    with left:
        st.image(show.img)
    with right:
        st.caption(show.desc)
        st.caption(f'Category: {show.category}')
    with super_right:
        st.button('👍🏼', key=random.random(), on_click=uic.activity, args=(show.index, 'Dislike'))
        st.button('👎🏼', key=random.random(), on_click=uic.activity, args=(show.index, 'Like'))
        st.button('⛔', key=random.random(), on_click=uic.activity, args=(show.index, 'DoNotShow'))



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
    uic.activity(int(id), 'Select Show')


def record_history(id):
    st.session_state[c.HISTORY].append(id)