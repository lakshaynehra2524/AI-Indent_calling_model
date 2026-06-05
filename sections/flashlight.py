import streamlit as st


def render():

    st.title("🔦 Flashlight")

    st.write("Flashlight turned on.")

    st.toggle(
        "Flashlight",
        value=True
    )