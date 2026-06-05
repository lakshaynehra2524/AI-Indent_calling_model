import streamlit as st


def render():

    st.title("😴 Sleep Tracker")

    st.write("Sleep section opened.")

    st.metric(
        "Today's Sleep",
        "7.5 Hours"
    )

    st.metric(
        "Sleep Quality",
        "Good"
    )