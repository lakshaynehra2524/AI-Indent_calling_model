import streamlit as st


def render():

    st.markdown(
        """
        <div style='
            text-align:center;
            margin-top:120px;
        '>

        <h1>
        🤖 AI Function Calling Assistant
        </h1>

        <h3 style='color:gray'>
        What would you like to do?
        </h3>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📞 Call")

        st.info("🎵 Music")

    with col2:
        st.info("📧 Mail")

        st.info("🏃 Running")

    with col3:
        st.info("😴 Sleep")

        st.info("🔦 Flashlight")