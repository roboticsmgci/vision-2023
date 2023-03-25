from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

# -----------------------------------------------------------
# (c) 2023 Grant O
# -----------------------------------------------------------


import cv2
from cscore import CameraServer, VideoSource
from networktables import NetworkTablesInstance
import extractor
import util
import socket
import json
import traceback
import time

server = socket.socket()
port = 5801
host = "10.85.74.71"
print("Host: " + str(host) + ", port: " + str(port))
ip = socket.gethostbyname(host)
print("IP: " + str(ip))

server.bind((host, port))
print("Awaiting socket connection...")
server.listen(2)
conn, address = server.accept()
print("Connection from: " + str(address))
try:
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
        #bin(str(str(len(april_tags)) + " apriltags detected"))

        # clientData = conn.recv(1024)
        # if len(clientData.decode()) > 0:
        #     print("client data: " + clientData.decode())
        conn.send((str(len(april_tags)) + " apriltags detected\n").encode())
        print(str(len(april_tags)) + " apriltags detected")
        result_img = frame.copy()
        draw_april_tags(result_img, april_tags)
        outputStream.putFrame(result_img)

except Exception:
    print(traceback.format_exc())
finally:
    server.shutdown(socket.SHUT_RDWR)
    server.close()
    print('socket server shutdown')
