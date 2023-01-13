# -----------------------------------------------------------
# (c) 2023 Grant O
# -----------------------------------------------------------

import extractor
import cv2

validIds = [1, 2, 3, 4, 5, 6, 7, 8]

vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)


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
        cv2.putText(image, str(tag.id), boundary.center, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(image, f'distance: {tag.directions.distance}', (boundary.center[0], boundary.center[1] + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


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
