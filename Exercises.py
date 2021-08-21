import cv2
import numpy as np
import time
import PoseModule as pm


cap = cv2.VideoCapture(0)
detector = pm.PoseDetector()

p_time = 0
counter = 0
direction = 0

while True:
    success, img = cap.read()
    # img = cv2.resize(img, (540, 960))
    # img = cv2.imread("videos/squatt.jpg")
    img = detector.find_pose(img, draw=True)
    lm_list = detector.get_position(img, False)
    if len(lm_list) != 0:
        angle = detector.find_angle(img, 11, 13, 15)  # trzy punkty do określenia kąta ze wzoru mediapipe
        squat_formula = (lm_list[13][2] - lm_list[11][2]) / (lm_list[15][2] - lm_list[13][2])
        percent = np.interp(angle, (170, 110), (0, 100))    # zakres ruchu w procentach
        # print(angle, percent)

        # if wykonanie przysiadu:
        if squat_formula > 0.9:
            if direction == 0:
                # counter += 0.5
                direction = 1
        if squat_formula < 0.4:
            if direction == 1:
                counter += 1
                direction = 0

        # wyświetlanie powtórzeń na obrazie
        cv2.putText(img, f"{counter}", (50, 200), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 5)

    # wyświetlanie fps
    # c_time = time.time()
    # fps =1/(c_time - p_time)
    # p_time = c_time
    # cv2.putText(img, f"{fps}", (50, 200), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 5)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
