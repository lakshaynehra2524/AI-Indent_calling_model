import streamlit as st


def render():

    st.title("🎵 Music Player")

    st.write("Music section opened.")

    song = st.text_input(
        "What do you want to play?"
    )

    st.button("▶ Play Music")

    