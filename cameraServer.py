# -----------------------------------------------------------
# (c) 2023 Grant O
# -----------------------------------------------------------

import cv2
from cscore import CameraServer, VideoSource
from networktables import NetworkTablesInstance
import extractor
import util

cap = cv2.VideoCapture(0)
cap.set(10, 0.1)
cs = CameraServer.getInstance()
outputStream = cs.putVideo("Cam1", 640, 480)

ntinst = NetworkTablesInstance.getDefault()
ntinst.startClientTeam(8574)
ret, frame = cap.read()

validIds = [1, 2, 3, 4, 5, 6, 7, 8]
def draw_april_tags(image, tags):
    for tag in tags:
        if tag.id not in validIds:  # probably random stuff from mistuned calibration
            continue
        boundary = tag.boundary
        cv2.line(image, boundary.bottomLeft,
                 boundary.bottomRight, (255, 255, 0), 4)
        cv2.line(image, boundary.bottomRight,
                 boundary.topRight, (255, 255, 0), 4)
        cv2.line(image, boundary.topRight,
                 boundary.topLeft, (255, 255, 0), 4)
        cv2.line(image, boundary.topLeft,
                 boundary.bottomLeft, (255, 255, 0), 4)
        util.centered_text(image, boundary.center, str(tag.id), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3, (0, 0))
        util.centered_text(image, boundary.center, f'{int(tag.directions.distance)}cm away', cv2.FONT_HERSHEY_SIMPLEX,
                           0.5, (255, 0, 0), 2, (0, 40))


while True:
    ret, frame = cap.read()
    april_tags = extractor.extract_april_tags(frame)
    result_img = frame.copy()
    draw_april_tags(result_img, april_tags)
    outputStream.putFrame(result_img)