import streamlit as st


def render():

    st.title("🏃 Running Dashboard")

    st.write(
        "Running mode opened successfully."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Distance",
        "0.0 km"
    )

    col2.metric(
        "Calories",
        "0 kcal"
    )

    col3.metric(
        "Duration",
        "0 min"
    )

    st.button("▶ Start Running")