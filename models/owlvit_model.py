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
    "adjustable dumbbell",
    "barbell",
    "bench",
    "incline bench",
    "flat bench",
    "incline bench",
    "flat bench",
    "weight plate",
    "cable machine",
    "lat pulldown machine",
    "lat pulldown machine",
    "smith machine",
    "kettlebell",
    "leg press machine",
    "squat rack",
    "power rack",
    "pull up bar",
    "resistance bands",
    "rowing machine",
    "exercise bike",
    "treadmill",
    "gym machine",
    "bench press station"
    "kettlebell",
    "leg press machine",
    "squat rack",
    "power rack",
    "pull up bar",
    "resistance bands",
    "rowing machine",
    "exercise bike",
    "treadmill",
    "gym machine",
    "bench press station"
]


def detect_objects(image):

    inputs = processor(
        text=[equipment_queries],
        images=image,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    target_sizes = torch.tensor(
        [image.size[::-1]]
    ).to(device)

    # WICHTIG: neue API
    results = processor.post_process_grounded_object_detection(
        outputs=outputs,
        target_sizes=target_sizes,
        threshold=0.15
    )

    detected = []

    boxes = results[0]["boxes"]
    scores = results[0]["scores"]
    labels = results[0]["labels"]

    for score, label in zip(
        scores,
        labels
    ):

        item = equipment_queries[
            label.item()
        ]

        if item not in detected:
            detected.append(item)

    return detected
