from transformers import CLIPProcessor
from transformers import CLIPModel
from PIL import Image
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
).to(device)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

equipment_labels = [
     "dumbbell",
    "adjustable dumbbell",
    "barbell",
    "bench",
    "incline bench",
    "flat bench",
    "weight plate",
    "cable machine",
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
]


def classify_equipment(image):

    inputs = processor(
        text=equipment_labels,
        images=image,
        return_tensors="pt",
        padding=True
    ).to(device)

    outputs = model(**inputs)

    logits = outputs.logits_per_image
    probs = logits.softmax(dim=1)

    confidence_threshold = 0.25

    detected = []

    for idx, prob in enumerate(probs[0]):
        score = prob.item()

        if score > confidence_threshold:
            detected.append(equipment_labels[idx])

    return detected
