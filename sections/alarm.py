import streamlit as st


def render():

    st.title("⏰ Alarm")

    st.write("Alarm section opened.")

    st.time_input(
        "Set Alarm Time"
    )

    st.button("Set Alarm")
    