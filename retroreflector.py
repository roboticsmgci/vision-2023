# -----------------------------------------------------------
# (c) 2023 Grant O
# -----------------------------------------------------------
# This is very unstable
# use with caution

import cv2
import logging
import numpy as np

validIds = [1, 2, 3, 4, 5, 6, 7, 8]

videoCaptureIndex = 1
if videoCaptureIndex == 1:
    logging.warning('Attempting to read from USB Camera: make sure it\'s connected')

vid = cv2.VideoCapture(videoCaptureIndex, cv2.CAP_DSHOW)

retro_lower_limit = np.array([252, 252, 252])
retro_higher_limit = np.array([255, 255, 255])
# 208,222,211 RGB
while True:
    ret, frame = vid.read()

    if frame is None:
        logging.error('Nothing to read from camera. Is the index correct?')
        break

    result_img = frame.copy()
    in_range = cv2.inRange(result_img, retro_lower_limit, retro_higher_limit)
    contours, _ = cv2.findContours(in_range, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 5:
            cv2.drawContours(result_img, [contour], 0, (255, 255, 0), 3)
    cv2.imshow('frame', frame)
    cv2.imshow('in_range', in_range)
    cv2.imshow('result', result_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
