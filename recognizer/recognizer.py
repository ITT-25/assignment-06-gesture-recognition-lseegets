from recognizer_helpers import normalize, load_template_points

GESTURES = ["rectangle", "circle", "check", "delete_mark", "pigtail"]
DIR = "xml_logs/s01/medium/"
SIZE = 100
NUM_POINTS = 64

templates = load_template_points(GESTURES, DIR)
normalized_templates = {}

for template in templates:
    normalized_points = normalize(templates[template], SIZE, NUM_POINTS)
    normalized_templates[template] = normalized_points