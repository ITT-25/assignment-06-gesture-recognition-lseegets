import math
from recognizer_helpers import load_template_points, normalize, distance_at_best_angle

GESTURES = ["rectangle", "circle", "check", "delete_mark", "pigtail"]
DIR = "xml_logs/s01/medium/"
SIZE = 100
NUM_POINTS = 64

templates = load_template_points(GESTURES, DIR)
normalized_templates = {}

for template in templates:
    normalized_points = normalize(templates[template], SIZE, NUM_POINTS)
    normalized_templates[template] = normalized_points


def recognize(input_points):
    points = normalize(input_points, SIZE, NUM_POINTS)
    b = math.inf
    match = None

    for name, template_points in normalized_templates.items():
        d = distance_at_best_angle(points, template_points)
        if d < b:
            b = d
            match = name
    return match