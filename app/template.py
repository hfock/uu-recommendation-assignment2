import constant as c
import streamlit as st
import pandas as pd

import random

from show import Show, ShowJson
import authenticate as auth
import user_interaction_collector as uic

from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


def sidebar(df_users, user_movie_dict):
    with st.sidebar:

        if st.session_state[c.SIMPSON] == c.LISA:
            st.session_state[c.MODE] = st.sidebar.radio('Go To', [c.HOME, c.HISTORY, c.ADVANCED])
        else:
            st.session_state[c.MODE] = st.sidebar.radio('Go To', [c.HOME, c.HISTORY])

        simpson_portrays()

        auth.authenticate(df_users, user_movie_dict)


def display_history(show: Show):
    left, right = st.columns([2, 2])

    with left:
        st.image(show.preview_img)
    with right:
        st.caption(show.desc)
        st.caption(f'Category: {show.category}')
        st.button('🕶', key=random.random(), on_click=select_show, args=(show.index, False,))


def display_show(show: Show):
    st.title(show.title)
    left, right, super_right = st.columns([2, 2, 1])
    with left:
        st.image(show.full_scale_img)
    with right:
        st.caption(show.desc)
        st.caption(f'Category: {show.category}')
    with super_right:
        rating = st.slider('How much did you like it?', 0, 10)
        st.button('Click me to indicate that you watched the content', key=random.random(),
                  on_click=uic.activity, args=(show.index, c.WATCHED, rating))


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
        st.image(item[c.DF_IMAGE_PREVIEW], use_column_width='always')

        st.markdown(f'''
        *{item[c.DF_CATEGORY]}*
        ##### {item["title"]}
        ''')


def select_show(id, history=True):
    if history:
        record_history(id)
    st.session_state[c.ID] = id
    uic.activity(int(id), 'Select Show')


def record_history(id):
    st.session_state[c.HISTORY].append(id)


def simpson_portrays():
    left, right = st.columns([2, 2])

    with left:
        st.button('📚', key=random.random(), on_click=select_simpson, args=(c.LISA,))
        if st.session_state[c.SIMPSON] == c.LISA:
            st.image(f'{c.DATA_PATH_SIMPSONS}lisa_selected.jpg')
        else:
            st.image(f'{c.DATA_PATH_SIMPSONS}lisa.png')
        if st.session_state[c.SIMPSON] == c.BART:
            st.image(f'{c.DATA_PATH_SIMPSONS}bart_selected.jpg')
        else:
            st.image(f'{c.DATA_PATH_SIMPSONS}bart.png')
        st.button('🛹', key=random.random(), on_click=select_simpson, args=(c.BART,))
    with right:
        st.button('🏡', key=random.random(), on_click=select_simpson, args=(c.MARGE,))
        if st.session_state[c.SIMPSON] == c.MARGE:
            st.image(f'{c.DATA_PATH_SIMPSONS}marge_selected.jpg')
        else:
            st.image(f'{c.DATA_PATH_SIMPSONS}marge.png')
        if st.session_state[c.SIMPSON] == c.HOMER:
            st.image(f'{c.DATA_PATH_SIMPSONS}homer_selected.jpg')
        else:
            st.image(f'{c.DATA_PATH_SIMPSONS}homer.png')
        st.button('🍩', key=random.random(), on_click=select_simpson, args=(c.HOMER,))


def select_simpson(simpson_name):
    st.session_state[c.SIMPSON] = simpson_name


def advanced_view(df_adv):
    selection = aggrid_interactive_table(df_adv)
    if selection:
        if selection["selected_rows"]:
            sel_show = ShowJson(selection["selected_rows"][0])
            st.session_state[c.ID] = sel_show.index
            st.markdown(f'''
            ## {sel_show.title}
            > {sel_show.desc}
            ***
            Category **{sel_show.category}** produced from the channel **{sel_show.channel}**

            Duration **{sel_show.duration} Minutes**
            ''')

            st.write('To watch the movie click the glasses')
            if st.button('🕶'):
                st.session_state[c.ID] = sel_show.index
                record_history(sel_show.index)


def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.
    Args:
        df (pd.DataFrame]): Source dataframe
    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )
    return selection
