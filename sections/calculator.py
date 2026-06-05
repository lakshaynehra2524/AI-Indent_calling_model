import streamlit as st


def render():

    st.title("🧮 Calculator")

    st.write("Calculator opened.")

    expression = st.text_input(
        "Enter expression"
    )

    st.button("Calculate")
    