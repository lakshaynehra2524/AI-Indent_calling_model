import streamlit as st


def render():

    st.title("📞 Calling Section")

    st.write("Call section opened.")

    st.text_input(
        "Whom do you want to call?"
    )

    st.button("Call")