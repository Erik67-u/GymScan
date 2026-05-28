equipment_map = {
    "incline bench": "bench",
    "flat bench": "bench",
    "adjustable dumbbell": "dumbbell",
    "bench press station": "bench",
    "lat pulldown machine":
        "cable machine",
    "power rack":
        "squat rack"
}


def normalize_equipment(
        equipment_list
):

    normalized = []

    for item in equipment_list:

        if item in equipment_map:
            normalized.append(
                equipment_map[item]
            )
        else:
            normalized.append(item)

    return list(set(normalized))