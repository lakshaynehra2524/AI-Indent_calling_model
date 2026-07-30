import smtplib
from email.message import EmailMessage

import streamlit as st

from core.config import SMTP_FROM, SMTP_HOST, SMTP_PASS, SMTP_PORT, SMTP_USER, smtp_configured


def _send_email(to_address, subject, body):
    message = EmailMessage()
    message["From"] = SMTP_FROM
    message["To"] = to_address
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(message)


def render():

    st.title("📧 Mailbox")

    entities = st.session_state.get("last_entities", {})

    receiver = st.text_input(
        "Recipient email",
        value=entities.get("recipient", "")
    )

    subject = st.text_input(
        "Subject",
        value=entities.get("subject", "")
    )

    message_body = st.text_area("Message")

    if not smtp_configured():
        st.info(
            "Demo mode - SMTP not configured. Add SMTP_HOST/SMTP_USER/SMTP_PASS "
            "to a local .env (see .env.example) to actually send mail."
        )

    if st.button("Send Mail"):

        if not receiver or not subject:
            st.warning("Recipient and subject are required.")
        elif not smtp_configured():
            st.warning("Preview only (SMTP not configured):")
            st.code(f"To: {receiver}\nSubject: {subject}\n\n{message_body}")
        else:
            try:
                _send_email(receiver, subject, message_body)
                st.success(f"Mail sent to {receiver}.")
            except Exception as exc:
                st.error(f"Failed to send mail: {exc}")
