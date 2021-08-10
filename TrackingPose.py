import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("videos/przysiad1.mp4")
detector = pm.PoseDetector()

while True:
    # success, img = cap.read()
    # img = cv2.resize(img, (360, 640))
    img = cv2.imread("videos/squatt.jpg")
    img = detector.find_pose(img, draw=False)
    lm_list = detector.get_position(img, False)
    if len(lm_list) != 0:
        detector.find_angle(img, 23, 25, 27)    #trzy punkty do określenia kąta ze wzoru mediapipe


    cv2.imshow("Image", img)
    cv2.waitKey(1)

