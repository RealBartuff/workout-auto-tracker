import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("videos/przysiad1.mp4")
detector = pm.PoseDetector()
counter = 0
direction = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (540, 960))
    # img = cv2.imread("videos/squatt.jpg")
    img = detector.find_pose(img, draw=False)
    lm_list = detector.get_position(img, False)
    if len(lm_list) != 0:
        # lewa noga
        angle = detector.find_angle(img, 23, 25, 27)    #trzy punkty do określenia kąta ze wzoru mediapipe
        # # prawa noga
        # detector.find_angle(img, 24, 26, 28)
        percent = np.interp(angle, (170, 110), (0, 100))    # zakres ruchu w procentach
        # print(angle, percent)

        # if wykonanie przysiadu:
        if percent == 100:
            if direction == 0:
                # counter += 0.5
                direction = 1
        if percent == 0:
            if direction == 1:
                counter += 1
                direction = 0
        print(counter)

        # wyświetlanie powtórzeń na obrazie
        cv2.putText(img, f"{counter}", (50, 200), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
