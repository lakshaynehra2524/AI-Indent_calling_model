import streamlit as st


def render():

    st.title("📧 Mailbox")

    st.write("Mail section opened.")

    receiver = st.text_input(
        "Whom to send mail?"
    )

    subject = st.text_input(
        "Subject"
    )

    message = st.text_area(
        "Message"
    )

    st.button("Send Mail")
