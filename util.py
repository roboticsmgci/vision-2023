# -----------------------------------------------------------
# (c) 2023 Grant O
# -----------------------------------------------------------

from math import sqrt
import cv2


def calculate_point_distance(p1, p2):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def centered_text(image, text, font, font_scale, color, thickness):
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    xCoord = int((image.shape[1] - text_size[0]) / 2)
    yCoord = int((image.shape[0] + text_size[1]) / 2)
    cv2.putText(image, text, (xCoord, yCoord), font, font_scale, color, thickness)


def centered_text(image, center, text, font, font_scale, color, thickness, offset):
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    xCoord = int(center[0] - (text_size[0] / 2)) + offset[0] if offset else 0
    yCoord = int(center[1] - (text_size[1] / 2)) + offset[1] if offset else 0
    cv2.putText(image, text, (xCoord, yCoord), font, font_scale, color, thickness)


# distance estimation
obj_distance = 100
obj_perceived_height = 102
obj_actual_height = 152


def get_focal_length():
    return (obj_perceived_height * obj_distance) / obj_actual_height


def estimate_distance(focal_length, height):
    return (obj_actual_height * focal_length) / height
