import streamlit as st
from PIL import Image

from services.detector import (
    detect_equipment
)

from services.recommender import (
    recommend_exercises
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="GymScan",
    page_icon="🏋️",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS DESIGN
# ---------------------------------------------------

st.markdown("""
<style>

/* Hintergrund Gradient */
.stApp {
    background:
    linear-gradient(
        135deg,
        #F8FBFF 0%,
        #EAF4FF 35%,
        #D7F4F5 70%,
        #EEF0FF 100%
    );
}

/* Haupttitel */
.main-title {
    font-size: 4rem;
    font-weight: 800;
    color: #1565C0;
    text-align: center;
    margin-bottom: 0;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #0284C7;
    font-size: 1.3rem;
    margin-top: 0;
    margin-bottom: 2rem;
}

/* Hero Box */
.hero-box {
    background:
    linear-gradient(
        135deg,
        rgba(31,182,255,0.15),
        rgba(0,194,184,0.12),
        rgba(139,92,246,0.10)
    );

    padding: 2rem;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    margin-bottom: 2rem;
}

/* Card Design */
.exercise-card {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(12px);
    border-radius: 22px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow:
        0 10px 30px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.4);
}

/* Exercise Title */
.exercise-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #1565C0;
    margin-bottom: 12px;
}

/* Text */
.exercise-text {
    color: #334155;
    font-size: 1rem;
}

/* Buttons */
div.stButton > button {
    width: 100%;
    background:
    linear-gradient(
        90deg,
        #1FB6FF,
        #00C2B8,
        #8B5CF6
    );

    color: white;
    border: none;
    border-radius: 16px;
    padding: 16px;
    font-size: 18px;
    font-weight: bold;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    transform: scale(1.02);
    box-shadow:
        0 10px 20px rgba(0,0,0,0.15);
}

/* Upload Box */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.65);
    border-radius: 18px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.5);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""
<div class="hero-box">

<h1 class="main-title">
🏋️ GymScan
</h1>

<p class="subtitle">
Train smarter.<br>
Scanne dein Equipment und entdecke passende Übungen.
</p>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# IMAGE UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "📸 Lade ein Bild deines Gym-Equipments hoch",
    type=["jpg", "jpeg", "png"]
)

# ---------------------------------------------------
# IMAGE PROCESSING
# ---------------------------------------------------

if uploaded_file:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    st.image(
        image,
        caption="Dein hochgeladenes Bild",
        use_container_width=True
    )

    if st.button(
        "🔍 Equipment scannen"
    ):

        with st.spinner(
            "GymScan analysiert dein Equipment..."
        ):

            equipment = detect_equipment(
                image
            )

            exercises = (
                recommend_exercises(
                    equipment
                )
            )

        st.success(
            "✅ Scan erfolgreich!"
        )

        # ---------------------------------------------------
        # DETECTED EQUIPMENT
        # ---------------------------------------------------

        st.markdown("## 🏋️ Erkanntes Equipment")

        if equipment:

            cols = st.columns(
                min(
                    len(equipment),
                    4
                )
            )

            for i, item in enumerate(
                equipment
            ):
                cols[
                    i % len(cols)
                ].success(
                    item.title()
                )

        else:
            st.warning(
                "Kein Equipment erkannt."
            )

        st.markdown("---")

        # ---------------------------------------------------
        # EXERCISES
        # ---------------------------------------------------

        st.markdown(
            "## 💪 Empfohlene Übungen"
        )

        if exercises:

            for ex in exercises:

                difficulty = ex[
                    "difficulty"
                ]

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

                <div class="exercise-text">

                <strong>🎯 Muskel:</strong>
                {ex["muscle"]}

                <br><br>

                <strong>🏋️ Muskelgruppe:</strong>
                {ex["muscle_group"]}

                <br><br>

                <strong>⚡ Schwierigkeit:</strong>
                {badge}
                {difficulty}

                <br><br>

                <strong>🛠 Equipment:</strong>
                {ex["equipment"]}

                <br><br>

                <strong>📖 Beschreibung:</strong><br>
                {ex["description"]}

                </div>
                </div>
                """, unsafe_allow_html=True)

        else:

            st.warning(
                "Keine Übungen gefunden."
            )