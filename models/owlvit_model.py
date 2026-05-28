from transformers import OwlViTProcessor
from transformers import OwlViTForObjectDetection
from PIL import Image
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = OwlViTProcessor.from_pretrained(
    "google/owlvit-base-patch32"
)

model = OwlViTForObjectDetection.from_pretrained(
    "google/owlvit-base-patch32"
).to(device)

equipment_queries = [
    "dumbbell",
    "barbell",
    "bench",
    "weight plate",
    "cable machine",
    "kettlebell",
    "smith machine"
]


def detect_objects(image):

    inputs = processor(
        text=[equipment_queries],
        images=image,
        return_tensors="pt"
    ).to(device)

    outputs = model(**inputs)

    target_sizes = torch.Tensor(
        [image.size[::-1]]
    )

    results = processor.post_process_object_detection(
        outputs=outputs,
        target_sizes=target_sizes,
        threshold=0.15
    )

    detected = []

    for box, score, label in zip(
        results[0]["boxes"],
        results[0]["scores"],
        results[0]["labels"]
    ):

        item = equipment_queries[label]

        if item not in detected:
            detected.append(item)

    return detected
