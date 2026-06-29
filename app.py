import streamlit as st
from PIL import Image

from services.detector import detect_equipment
from services.recommender import recommend_exercises

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="GymScan",
    page_icon="🏋️",
    layout="wide"
)

# ---------------------------------------------------
# CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* =====================================================
   FONT
===================================================== */

@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800&display=swap');

html,
body,
[data-testid="stAppViewContainer"] * {
    font-family: 'Exo 2', sans-serif !important;
}

/* =====================================================
   STREAMLIT AUSBLENDEN
===================================================== */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stToolbar"] {
    display:none;
}

[data-testid="collapsedControl"] {
    display:none;
}

/* =====================================================
   HINTERGRUND
===================================================== */

.stApp {
    background:
    linear-gradient(
        180deg,
        #070B1A 0%,
        #0B1022 45%,
        #0E1430 100%
    );
}

/* =====================================================
   LAYOUT
===================================================== */

.block-container {
    max-width:1300px;
    padding-top:1rem;
}

/* =====================================================
   HERO
===================================================== */

.hero-card {

    background:
    linear-gradient(
        135deg,
        #162447,
        #1F4068,
        #2B5876
    );

    padding:40px;
    border-radius:30px;

    box-shadow:
    0px 0px 30px rgba(
        77,
        166,
        255,
        0.20
    );

    margin-bottom:30px;
}

.hero-title {

    color:white;
    font-size:58px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:2px;

}

.hero-subtitle {

    color:#A5D8FF;
    font-size:20px;
    margin-top:10px;

}

/* =====================================================
   TITEL
===================================================== */

.section-title {

    color:white;
    font-size:30px;
    font-weight:700;
    margin-top:20px;
    margin-bottom:20px;

}

/* =====================================================
   EQUIPMENT CARD
===================================================== */

.equipment-card {

    background:#111827;

    padding:20px;

    border-radius:18px;

    margin-bottom:15px;

    border:1px solid #1E3A8A;

    color:white;

    text-align:center;

    font-size:18px;

    font-weight:700;

}

/* =====================================================
   EXERCISE CARD
===================================================== */

.exercise-card {

    background:#111827;

    padding:25px;

    border-radius:25px;

    margin-bottom:20px;

    border:1px solid rgba(
        77,
        166,
        255,
        0.20
    );

    box-shadow:
    0px 0px 20px rgba(
        77,
        166,
        255,
        0.08
    );

}

.exercise-title {

    color:white;

    font-size:26px;

    font-weight:700;

    margin-bottom:15px;

}

.exercise-text {

    color:#D1D5DB;

    line-height:1.8;

}

/* =====================================================
   MUSCLE CHIP
===================================================== */

.muscle-chip {

    background:#1E3A8A;

    padding:8px 16px;

    border-radius:999px;

    color:white;

    font-size:14px;

    display:inline-block;

    margin-bottom:15px;

}

/* =====================================================
   BUTTON
===================================================== */

div.stButton > button {

    background:
    linear-gradient(
        90deg,
        #3B82F6,
        #06B6D4
    );

    color:white;

    border:none;

    border-radius:18px;

    height:60px;

    width:100%;

    font-size:18px;

    font-weight:700;

    transition:0.3s;

}

div.stButton > button:hover {

    transform:scale(1.02);

    box-shadow:
    0px 0px 25px rgba(
        59,
        130,
        246,
        0.4
    );

}

/* =====================================================
   FILE UPLOADER
===================================================== */

[data-testid="stFileUploader"] {

    background:#111827;

    border:1px solid #1E3A8A;

    border-radius:20px;

    padding:20px;

}

/* Verhindert doppelte Upload-Anzeige */

[data-testid="stFileUploader"] section button p {
    display:none;
}

/* =====================================================
   SUCCESS
===================================================== */

[data-testid="stSuccess"] {

    background:#102A43;

}

/* =====================================================
   SCROLLBAR
===================================================== */

::-webkit-scrollbar {
    width:8px;
}

::-webkit-scrollbar-track {
    background:#070B1A;
}

::-webkit-scrollbar-thumb {
    background:#1E3A8A;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HERO
# ---------------------------------------------------

st.markdown("""
<div class="hero-card">

<div class="hero-title">
🏋️ GymScan
</div>

<div class="hero-subtitle">
KI-gestützte Equipment-Erkennung für dein Training.<br>
Scanne dein Equipment und erhalte passende Übungen in Sekunden.
</div>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "📸 Lade ein Bild hoch",
    type=["jpg", "jpeg", "png"]
)

# ---------------------------------------------------
# PROCESS IMAGE
# ---------------------------------------------------

if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        use_container_width=True
    )

    if st.button("🔍 Equipment scannen"):

        with st.spinner("GymScan analysiert dein Bild..."):

            equipment = detect_equipment(image)

            exercises = recommend_exercises(
                equipment
            )

        st.success("✅ Scan abgeschlossen")

        # Equipment

        st.markdown(
            '<div class="section-title">🏋️ Erkanntes Equipment</div>',
            unsafe_allow_html=True
        )

        if equipment:

            for item in equipment:

                st.markdown(f"""
                <div class="equipment-card">
                {item.title()}
                </div>
                """, unsafe_allow_html=True)

        else:

            st.warning(
                "Kein Equipment erkannt."
            )

        # Übungen

        st.markdown(
            '<div class="section-title">💪 Empfohlene Übungen</div>',
            unsafe_allow_html=True
        )

        if exercises:

            for ex in exercises:

                difficulty = ex.get(
                    "difficulty",
                    "Anfänger"
                )

                if difficulty == "Anfänger":
                    badge = "🟢"
                elif difficulty == "Fortgeschritten":
                    badge = "🔵"
                else:
                    badge = "🟣"

                st.markdown(f"""
                <div class="exercise-card">

                <div class="exercise-title">
                {ex["name"]}
                </div>

                <span class="muscle-chip">
                {ex["muscle_group"]}
                </span>

                <div class="exercise-text">

                🎯 <b>Muskel:</b> {ex["muscle"]}

                <br><br>

                ⚡ <b>Schwierigkeit:</b>
                {badge} {difficulty}

                <br><br>

                🏋️ <b>Equipment:</b>
                {ex["equipment"]}

                <br><br>

                📖 <b>Beschreibung:</b><br>
                {ex["description"]}

                </div>

                </div>
                """, unsafe_allow_html=True)

        else:

            st.warning(
                "Keine Übungen gefunden."
            )