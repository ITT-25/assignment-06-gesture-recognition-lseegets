import math
import os
import xml.etree.ElementTree as ET


def load_template_points(gestures, directory):
    templates = {}

    for gesture in gestures:
        filename = f"{gesture}01.xml"
        filepath = os.path.join(directory, filename)
        tree = ET.parse(filepath)
        root = tree.getroot()

        points = []
        for point in root.findall("Point"):
            points.append((float(point.attrib["X"]), float(point.attrib["Y"])))
        templates[gesture] = points

    return templates 

def normalize(points, size, n):
    resampled_points = resample(points, n)
    angle = indicative_angle(resampled_points)
    rotated_points = rotate_by(resampled_points, -angle)
    scaled_points = scale_to(rotated_points, size)
    return translate_to_origin(scaled_points)


# Helper functions
# Code is based on this source code: https://depts.washington.edu/acelab/proj/dollar/dollar.js
# And this pseudo-code: https://depts.washington.edu/acelab/proj/dollar/dollar.pdf

def distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[0] - p1[0]
    return math.sqrt(dx*dx + dy*dy)


def path_length(points):
    d = 0
    for i in range(1, len(points)):
        d += distance(points[i-1], points[i])
    return d


def resample(points, n):
    I = path_length(points) / (n-1)
    D  = 0
    new_points = [points[0]]
    i = 1
    while i < len(points):
        d = distance(points[i-1], points[i])
        if D + d >= I:
            qx = points[i-1][0] + ((I - D) / d) * (points[i][0] - points[i-1][0])
            qy = points[i-1][1] + ((I - D) / d) * (points[i][1] - points[i-1][1])
            q = (qx, qy)
            new_points.append(q)
            points.insert(i, q)
            D = 0
            i += 1
        else:
            D += d
            i += 1

    if len(new_points) == n-1:
        new_points.append(points[-1])

    return new_points


def centroid(points):
    x_sum = 0
    y_sum = 0
    n = len(points)
    for point in points:
        x_sum += point[0]
        y_sum += point[1]
    return x_sum/n, y_sum/n


def indicative_angle(points):
    cx, cy = centroid(points)
    x_1, y_1 = points[0]
    return math.atan2(cy - y_1, cx - x_1)


def rotate_by(points, angle):
    new_points = []
    cx, cy = centroid(points)
    for point in points:
        qx = (point[0] - cx) * math.cos(angle) - (point[1] - cy) * math.sin(angle) + cx
        qy = (point[0] - cx) * math.sin(angle) + (point[1] - cy) * math.cos(angle) + cy
        new_points.append((qx, qy))
    return new_points


def scale_to(points, size):
    # Corner points of the bounding box
    x_values = []
    y_values = []
    for point in points:
        x_values.append(point[0])
        y_values.append(point[1])
    min_x = min(x_values)
    max_x = max(x_values)
    min_y = min(y_values)
    max_y = max(y_values)

    # Width and height of the bounding box
    width = max_x - min_x
    height = max_y - min_y

    new_points = []
    for point in points:
        qx = (point[0] - min_x) * size / width
        qy = (point[1] - min_y) * size / height
        new_points.append((qx, qy))

    return new_points


def translate_to_origin(points):
    cx, cy = centroid(points)
    new_points = []
    for point in points:
        qx = point[0] - cx
        qy = point[1] - cy
        new_points.append((qx, qy))
    return new_points


def distance_at_best_angle(points, template_points, angle_lower=-math.radians(45), angle_upper=math.radians(45), threshold=math.radians(2)):
    phi = 0.5 * (-1 + math.sqrt(5))
    x1 = phi * angle_lower + (1 - phi) * angle_upper
    f1 = distance_at_angle(points, template_points, x1)
    x2 = (1 - phi) * angle_lower + phi * angle_upper
    f2 = distance_at_angle(points, template_points, x2)

    while abs(angle_lower - angle_upper) > threshold:
        if f1 < f2:
            angle_upper = x2
            x2 = x1
            f2 = f1
            x1 = phi * angle_lower + (1 - phi) * angle_upper
            f1 = distance_at_angle(points, template_points, x1)
        else:
            angle_lower = x1
            x1 = x2
            f1 = f2
            x2 = (1 - phi) * angle_lower + phi * angle_upper
            f2 = distance_at_angle(points, template_points, x2)

    return min(f1, f2)


def path_distance(a, b):
    d = 0
    for i in range(0, len(a)):
        d += math.dist(a[i], b[i])
    return d / len(a)
    

def distance_at_angle(points, template_points, angle):
    new_points = rotate_by(points, angle)
    return path_distance(new_points, template_points)