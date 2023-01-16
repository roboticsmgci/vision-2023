# -----------------------------------------------------------
# (c) 2023 Grant O
# -----------------------------------------------------------

import cv2
from pupil_apriltags import Detector
from boundary import Boundary
from apriltag import AprilTag
from directions import Directions
import util

at_detector = Detector(
    families="tag16h5",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=4.0,
    refine_edges=1,
    decode_sharpening=0,
    debug=0
)

focal_length = util.get_focal_length()


def extract_boundary(tag):
    center = tag.center
    corners = tag.corners

    center = (int(center[0]), int(center[1]))
    topLeftCorner = (int(corners[3][0]), int(corners[3][1]))
    topRightCorner = (int(corners[2][0]), int(corners[2][1]))
    bottomLeftCorner = (int(corners[0][0]), int(corners[0][1]))
    bottomRightCorner = (int(corners[1][0]), int(corners[1][1]))
    return Boundary(topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner, center)


def extract_directions(tag, boundary):
    avg_top_y = (boundary.topLeft[1] + boundary.topRight[1]) / 2
    avg_top_x = (boundary.topLeft[0] + boundary.topRight[0]) / 2
    avg_bottom_y = (boundary.bottomLeft[1] + boundary.bottomRight[1]) / 2
    avg_bottom_x = (boundary.bottomLeft[0] + boundary.bottomRight[0]) / 2
    height = util.calculate_point_distance((avg_top_x, avg_top_y), (avg_bottom_x, avg_bottom_y))
    estimated_distance = util.estimate_distance(focal_length, height) if height > 0 else -1

    return Directions(height, estimated_distance)


def extract_april_tags(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected = at_detector.detect(gray)

    tags = []
    for detectedTag in detected:
        boundary = extract_boundary(detectedTag)
        directions = extract_directions(detectedTag, boundary)
        tags.append(AprilTag(detectedTag.tag_id, boundary, directions))
    return tags
