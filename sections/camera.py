from datetime import datetime

import streamlit as st

from core.config import CAPTURES_DIR


def render():

    st.title("📷 Camera")

    photo = st.camera_input("Take a picture")

    if photo is not None:

        CAPTURES_DIR.mkdir(parents=True, exist_ok=True)

        filename = f"capture_{datetime.now():%Y%m%d_%H%M%S}.jpg"
        path = CAPTURES_DIR / filename
        path.write_bytes(photo.getvalue())

        st.success(f"Saved to captures/{filename}")
