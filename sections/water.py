import streamlit as st


def render():

    st.title("💧 Water Tracker")

    st.write("Track hydration.")

    st.number_input(
        "Water intake (ml)",
        min_value=0
    )

    st.button("Save")