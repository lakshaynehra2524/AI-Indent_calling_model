import streamlit as st

from core.audio import generate_tone_wav
from core.config import MUSIC_DIR

_PLACEHOLDER_NAME = "demo_tone.wav"


def _ensure_placeholder_track():
    MUSIC_DIR.mkdir(parents=True, exist_ok=True)
    placeholder_path = MUSIC_DIR / _PLACEHOLDER_NAME

    if not placeholder_path.exists():
        placeholder_path.write_bytes(
            generate_tone_wav(frequency=523.25, duration_seconds=2.0)
        )


def render():

    st.title("🎵 Music Player")

    _ensure_placeholder_track()

    tracks = sorted(p.name for p in MUSIC_DIR.iterdir() if p.is_file())

    entities = st.session_state.get("last_entities", {})
    query = entities.get("query", "")

    default_index = 0
    if query:
        for i, track in enumerate(tracks):
            if query.lower() in track.lower():
                default_index = i
                break

    if query:
        st.caption(
            f'Heard "play {query}" - pick from your library below '
            "(drop your own files into assets/music/)."
        )

    selection = st.selectbox("Choose a track", tracks, index=default_index)

    if st.button("▶ Play Music"):
        st.audio((MUSIC_DIR / selection).read_bytes())
