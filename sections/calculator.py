import streamlit as st

from core.safe_math import UnsafeExpressionError, safe_eval


def render():

    st.title("🧮 Calculator")

    entities = st.session_state.get("last_entities", {})

    expression = st.text_input(
        "Enter expression",
        value=entities.get("expression", "")
    )

    if st.button("Calculate"):

        if not expression:
            st.warning("Enter an expression first.")
        else:
            try:
                result = safe_eval(expression)
                st.success(f"{expression} = {result}")
            except UnsafeExpressionError as exc:
                st.error(f"Couldn't evaluate that: {exc}")
