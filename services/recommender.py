import json


def recommend_exercises(
        detected_equipment
):

    with open(
        "database/exercises.json",
        "r"
    ) as file:

        database = json.load(file)

    exercises = []

    for equipment in detected_equipment:

        if equipment in database:
            exercises.extend(
                database[equipment]
            )

    return exercises
