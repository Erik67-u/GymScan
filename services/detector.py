from models.clip_model import classify_equipment
from models.owlvit_model import detect_objects


def detect_equipment(image):

    owl_results = detect_objects(image)

    clip_results = classify_equipment(image)

    final_equipment = list(
        set(owl_results + clip_results)
    )

    return final_equipment

