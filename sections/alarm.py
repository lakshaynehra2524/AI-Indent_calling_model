from datetime import datetime, timedelta

import streamlit as st

from core.audio import generate_tone_wav


def _play_beep():
    st.audio(
        generate_tone_wav(frequency=880, duration_seconds=0.5),
        format="audio/wav",
        autoplay=True
    )


def render():

    st.title("⏰ Alarm")

    if "alarm_target" not in st.session_state:
        st.session_state.alarm_target = None

    entities = st.session_state.get("last_entities", {})

    detected_label = None
    if "duration_minutes" in entities:
        detected_label = f"in {entities['duration_minutes']} minute(s)"
    elif "hour" in entities:
        detected_label = f"at {entities['hour']:02d}:{entities['minute']:02d}"

    if detected_label:
        st.caption(f"Detected from your command: {detected_label}")

        if st.button("Use detected time"):
            if "duration_minutes" in entities:
                st.session_state.alarm_target = datetime.now() + timedelta(
                    minutes=entities["duration_minutes"]
                )
            else:
                target = datetime.now().replace(
                    hour=entities["hour"],
                    minute=entities["minute"],
                    second=0,
                    microsecond=0
                )
                if target <= datetime.now():
                    target += timedelta(days=1)
                st.session_state.alarm_target = target

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        manual_minutes = st.number_input(
            "Or set manually - minutes from now",
            min_value=1,
            value=5
        )

        if st.button("Set Alarm"):
            st.session_state.alarm_target = datetime.now() + timedelta(
                minutes=manual_minutes
            )

    with col2:
        if st.session_state.alarm_target and st.button("Cancel Alarm"):
            st.session_state.alarm_target = None

    if st.session_state.alarm_target:
        remaining = st.session_state.alarm_target - datetime.now()

        if remaining.total_seconds() <= 0:
            st.error("⏰ Time's up!")
            st.balloons()
            _play_beep()
        else:
            minutes, seconds = divmod(int(remaining.total_seconds()), 60)
            st.metric("Time remaining", f"{minutes:02d}:{seconds:02d}")
            st.caption(
                "Interact with the app (or send another command) to refresh the countdown."
            )
    else:
        st.info("No alarm set.")
