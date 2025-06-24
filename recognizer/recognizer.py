import math
from recognizer_helpers import normalize, distance_at_best_angle
from templates import templates

SIZE = 100
NUM_POINTS = 64

normalized_templates = {}


# Normalize the templates

for template in templates:
    normalized_points = normalize(templates[template], SIZE, NUM_POINTS)
    normalized_templates[template] = normalized_points


# Recognize the input gesture

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