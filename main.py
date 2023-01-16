# -----------------------------------------------------------
# (c) 2023 Grant O
# -----------------------------------------------------------

import extractor
import cv2
import logging

import util

validIds = [1, 2, 3, 4, 5, 6, 7, 8]

videoCaptureIndex = 0
if videoCaptureIndex == 1:
    logging.warning('Attempting to read from USB Camera: make sure it\'s connected')

vid = cv2.VideoCapture(videoCaptureIndex, cv2.CAP_DSHOW)


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
    ret, frame = vid.read()
    april_tags = extractor.extract_april_tags(frame)
    result_img = frame.copy()
    draw_april_tags(result_img, april_tags)
    cv2.imshow('frame', result_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
