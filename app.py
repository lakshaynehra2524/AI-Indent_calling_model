# Importing libraries and dependencies
import streamlit as st
from core.entities import extract_entities
from core.logging_store import log_prediction
from core.predictor import predict_intent
from core.router import route_intent

from sections import (
    home,
    running,
    call,
    mail,
    camera,
    music,
    alarm,
    calculator,
    water,
    sleep,
    flashlight,
    analytics
)

# Page settings

st.set_page_config(
    page_title="AI-Assistant",
    layout="wide"
)

# Handling session state

if "active_section" not in st.session_state:
    st.session_state.active_section = "home"

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

if "last_intent" not in st.session_state:
    st.session_state.last_intent = None

if "last_confidence" not in st.session_state:
    st.session_state.last_confidence = None

if "last_entities" not in st.session_state:
    st.session_state.last_entities = {}

if "last_fallback" not in st.session_state:
    st.session_state.last_fallback = False


# Side bar config.


with st.sidebar:

    st.title("🤖 Assistant")

    st.caption(
        "AI Powered Function Calling"
    )

    st.divider()

    st.markdown("### Sections")

    sections = {

        "🏠 Home": "home",
        "📞 Call": "call",
        "📧 Mail": "mail",
        "📷 Camera": "camera",
        "🎵 Music": "music",
        "⏰ Alarm": "alarm",
        "🧮 Calculator": "calculator",
        "🏃 Running": "running",
        "💧 Water": "water",
        "😴 Sleep": "sleep",
        "🔦 Flashlight": "flashlight",
        "📊 Analytics": "analytics"
    }

    for label, section in sections.items():

        if st.button(
            label,
            use_container_width=True
        ):

            st.session_state.active_section = (
                section
            )

            st.rerun()

    st.divider()

    st.markdown("### Recent Commands")

    if len(
        st.session_state.chat_history
    ) == 0:

        st.caption(
            "No commands yet."
        )

    else:

        for cmd in reversed(
            st.session_state.chat_history[-8:]
        ):

            st.info(cmd)



# Active session
# PREMIUM ACTIVE SECTION CARD

if st.session_state.last_confidence is None:
    badge_label = "● LIVE"
    badge_color = "#2563EB"
elif st.session_state.last_fallback:
    badge_label = "🤔 NOT SURE"
    badge_color = "#B45309"
else:
    badge_label = f"{st.session_state.last_confidence * 100:.0f}% CONFIDENT"
    badge_color = "#15803D"

if st.session_state.last_entities:
    entities_text = " · ".join(
        f"{key}: {value}" for key, value in st.session_state.last_entities.items()
    )
else:
    entities_text = "no slots extracted"

st.markdown(f"""
<div style="
    background:#151922;
    border:1px solid rgba(255,255,255,0.08);
    border-radius:18px;
    padding:16px 24px;
    margin-bottom:18px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.2);
">

<div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
">

<div>
<p style="
    margin:0;
    font-size:12px;
    color:#9CA3AF;
    text-transform:uppercase;
    letter-spacing:1px;
">
ACTIVE SECTION
</p>

<h3 style="
    margin:0;
    margin-top:5px;
    color:white;
">
{st.session_state.active_section.title()}
</h3>

<p style="
    margin:0;
    margin-top:6px;
    font-size:12px;
    color:#9CA3AF;
">
{entities_text}
</p>
</div>

<div style="
    background:{badge_color};
    color:white;
    padding:8px 14px;
    border-radius:12px;
    font-size:12px;
    font-weight:600;
    white-space:nowrap;
">
{badge_label}
</div>

</div>
</div>
""", unsafe_allow_html=True)

# Render active screen 


if st.session_state.active_section == "home":
    home.render()

elif st.session_state.active_section == "running":
    running.render()

elif st.session_state.active_section == "call":
    call.render()

elif st.session_state.active_section == "mail":
    mail.render()

elif st.session_state.active_section == "camera":
    camera.render()

elif st.session_state.active_section == "music":
    music.render()

elif st.session_state.active_section == "alarm":
    alarm.render()

elif st.session_state.active_section == "calculator":
    calculator.render()

elif st.session_state.active_section == "water":
    water.render()

elif st.session_state.active_section == "sleep":
    sleep.render()

elif st.session_state.active_section == "flashlight":
    flashlight.render()

elif st.session_state.active_section == "analytics":
    analytics.render()


# Chatgpt style input 
st.markdown("---")

user_input = st.chat_input(
    "Type your command..."
)


# Prediction

if user_input:

    st.session_state.chat_history.append(
        user_input
    )

    predicted_intent, confidence = predict_intent(
        user_input
    )

    entities = extract_entities(
        user_input, predicted_intent
    )

    next_page = route_intent(
        predicted_intent, confidence
    )

    log_prediction(
        user_input, predicted_intent, confidence, entities, next_page
    )

    st.session_state.chat_history.append(
        f"Opened section: {next_page}"
    )

    st.session_state.last_intent = predicted_intent
    st.session_state.last_confidence = confidence
    st.session_state.last_entities = entities
    st.session_state.last_fallback = (
        next_page == "home" and predicted_intent != "home"
    )

    st.session_state.active_section = (
        next_page
    )

    st.rerun()

# Background 



st.markdown("""
<style>

/* Main app background */
.stApp {
    background: linear-gradient(
        135deg,
        #020617 0%,
        #0F172A 40%,
        #111827 100%
    );
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background: #1A1D29;
}

</style>
""", unsafe_allow_html=True)
