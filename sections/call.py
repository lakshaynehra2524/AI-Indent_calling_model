import streamlit as st

from core.contacts import lookup_contact


def render():

    st.title("📞 Calling Section")

    entities = st.session_state.get("last_entities", {})

    name = st.text_input(
        "Whom do you want to call?",
        value=entities.get("contact", "")
    )

    resolved_number = entities.get("phone") or lookup_contact(name)

    if name and not resolved_number:
        st.warning(
            f'"{name}" isn\'t in the demo contact book (core/contacts.py).'
        )
        resolved_number = st.text_input("Enter a phone number instead")

    if resolved_number:
        st.markdown(
            f'<a href="tel:{resolved_number}" style="text-decoration:none;">'
            f'<button style="padding:10px 18px;border-radius:10px;border:none;'
            f'background:#2563EB;color:white;font-weight:600;cursor:pointer;">'
            f"📞 Call {name or resolved_number}"
            f"</button></a>",
            unsafe_allow_html=True
        )
        st.caption(
            "This is a real tel: link - it opens your device's dialer "
            "(works on phones and most desktops with a calling app registered)."
        )
