import cv2
import time
import PoseModule as pm

cap = cv2.VideoCapture("videos/test.mp4")
    pTime = 0
    detector = pm.PoseDetector()
    while True:
        success, img = cap.read()
        img = detector.find_pose(img)
        lm_list = detector.find_pose(img)
        print(lm_list)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0),
                    3)  # trzy wartosci w nawiasach to kolory rgb
        cv2.imshow("Image", img)

        cv2.waitKey(1)