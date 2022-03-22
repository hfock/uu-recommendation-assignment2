import constant as c
import streamlit as st
import pandas as pd

from CurrentShow import CurShow, CurShowJson

from random import random

from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


def display_selected_item(cur_show: CurShow):
    st.title(cur_show.title)
    left, middle, right = st.columns([1, 3,  1])
    with middle:
        st.image(cur_show.img)
    st.caption(cur_show.desc)
    st.caption(f'Category: {cur_show.category}')


def display_history(cur_show: CurShow):
    left, right = st.columns([2, 2])

    with left:
        st.image(cur_show.img)
    with right:
        st.caption(cur_show.desc)
        st.caption(f'Category: {cur_show.category}')
        st.button('🕶', key=random(), on_click=select_show, args=(cur_show.index, False,))


def recommendations(df, text=None):
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
        st.button('🕶', key=random(), on_click=select_show, args=(item['index'],))
        st.image(item['img'], use_column_width='always')
        st.markdown(f'''
        *{item["category"]}*
        ##### {item["title"]}
        ''')


def record_history(id):
    if not st.session_state[c.PRIVACY]:
        st.session_state[c.HISTORY].append(id)


def select_show(id, history=True):
    if history:
        record_history(id)
    st.session_state[c.ID] = id


def sidebar(df):
    st.sidebar.info('This is a mid-fidelity prototype. It is not possible to play any video.')
    st.session_state[c.MODE] = st.sidebar.radio('Go To', [c.EXPLORE, c.ADVANCED, c.HISTORY])
    st.session_state[c.GENRE_FILTER] = genre_filter = st.sidebar.checkbox('Genre')
    if genre_filter:
        st.session_state[c.GENRE] = st.sidebar.selectbox('Genre', df['category'].sort_values().unique())
    st.session_state[c.PRIVACY] = st.sidebar.checkbox('Privacy Mode')
    if st.session_state[c.TRANSPARENCY]:
        if st.session_state[c.PRIVACY]:
            st.sidebar.info('You are now in the privacy mode, '
                            'nothing is now recorded from you, but you cannot use the features that need your data.')
    st.session_state[c.DIVERSITY] = st.sidebar.checkbox('Diversity Mode', value=True)
    if st.session_state[c.TRANSPARENCY]:
        if st.session_state[c.DIVERSITY]:
            st.sidebar.info('You are now in the diversity mode, '
                            'On your casual browsing view you now witness recommendations that are still based '
                            'on the content you have selected at the moment but in a '
                            'more broad horizon extending manner.')
    st.session_state[c.TRANSPARENCY] = st.sidebar.checkbox('Transparency Mode')
    if st.session_state[c.TRANSPARENCY]:
        st.sidebar.info('You are now in the transparency mode, you will see information like this in many occasions.'
                        'The brief explanation should help you understand what is what doing and why.')


def exploration(df_adv):
    selection = aggrid_interactive_table(df_adv)
    if selection:
        if selection["selected_rows"]:
            sel_show = CurShowJson(selection["selected_rows"][0])
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
                st.session_state[c.MODE] = c.EXPLORE
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
