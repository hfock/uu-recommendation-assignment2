import streamlit as st
import json
import datetime

import constant as c


# save the activities as a file
def save_activities():
    with open(f'{c.DATA_PATH}activities.json', 'w') as outfile:
        json.dump(st.session_state[c.ACTIVITIES], outfile, indent=4)


# function that processes an activity
def activity(id, activity, watch_percentage = None):
    print(watch_percentage)
    data = {'content_id': int(id),
            'activity': activity,
            'watch_percentage': watch_percentage,
            'user_id': st.session_state['user'],
            'datetime': str(datetime.datetime.now())}
    # add to the session state
    st.session_state[c.ACTIVITIES].append(data)
    # directly save the activities
    save_activities()
