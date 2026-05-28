import streamlit as st
from PIL import Image

from services.detector import (
    detect_equipment
)

from services.recommender import (
    recommend_exercises
)

st.set_page_config(
    page_title="GymScan",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ GymScan")

st.write(
    "Upload gym equipment and get exercises."
)

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image"
    )

    if st.button(
        "Scan Equipment"
    ):

        with st.spinner(
            "Scanning..."
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
            "Scan Complete"
        )

        st.subheader(
            "Detected Equipment"
        )

        for item in equipment:
            st.write(f"✅ {item}")

        st.subheader(
            "Recommended Exercises"
        )

        for ex in exercises:

            with st.expander(
                ex["name"]
            ):

                st.write(
                    f"Muscle: {ex['muscle']}"
                )

                st.write(
                    f"Difficulty: {ex['difficulty']}"
                )

                st.write(
                    ex["description"]
                )