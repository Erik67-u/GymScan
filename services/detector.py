from models.clip_model import (
    classify_equipment
)

from models.owlvit_model import (
    detect_objects
)

from utils.equipment_mapper import (
    normalize_equipment
)


def detect_equipment(image):

    # OWL-ViT Detection
    owl_results = detect_objects(
        image
    )

    # CLIP Classification
    clip_results = classify_equipment(
        image
    )

    # Combine both models
    combined_results = list(
        set(
            owl_results +
            clip_results
        )
    )

    # Normalize names
    final_equipment = (
        normalize_equipment(
            combined_results
        )
    )

    return final_equipment
