import pandas as pd
import streamlit as st

from core.logging_store import get_recent, get_stats


def render():

    st.title("📊 Analytics")

    stats = get_stats()

    if stats["total"] == 0:
        st.info("No commands logged yet - try typing something in the chat box below.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total commands", stats["total"])
    col2.metric("Avg. confidence", f"{stats['avg_confidence'] * 100:.0f}%")
    col3.metric("Fell back to Home", stats["fallback_count"])

    st.subheader("Commands by intent")
    st.bar_chart(pd.DataFrame({"count": stats["by_intent"]}))

    st.subheader("Recent commands")
    for entry in get_recent(10):
        st.write(
            f"**{entry['intent']}** ({entry['confidence'] * 100:.0f}%) - "
            f"\"{entry['text']}\" → {entry['route']} · {entry['entities']}"
        )
