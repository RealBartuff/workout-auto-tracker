import kivy

kivy.require('2.0.0')

import kivy.core.text
import numpy as np
import time
import PoseModule as pm
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2

detector = pm.PoseDetector()


class WindowManager(ScreenManager):
    pass


class Menu(Screen):
    pass


class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.cap = None
        self.push_counter = 0
        self.sit_counter = 0
        self.direction = 0
        self.event = None

    def start(self, cap, fps=30):
        self.cap = cap
        self.event = Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        if self.event:
            Clock.unschedule(self.event)
        self.cap = None

    def update(self, dt):
        return_value, frame = self.cap.read()
        img = detector.find_pose(frame, draw=True)
        lm_list = detector.get_position(frame, False)
        if len(lm_list) != 0:
            angle1 = detector.find_angle(img, 11, 13, 15)
            angle2 = detector.find_angle(img, 23, 25, 27)# trzy punkty do określenia kąta ze wzoru mediapipe
            pushup_formula = (lm_list[13][2] - lm_list[11][2]) / (lm_list[15][2] - lm_list[13][2])
            squat_formula = (lm_list[25][2] - lm_list[23][2]) / (lm_list[27][2] - lm_list[25][2])
            # percent = np.interp(angle, (170, 110), (0, 100))  # zakres ruchu w procentach
            if squat_formula > 0.9:
                if self.direction == 0:
                    # counter += 0.5
                    self.direction = 1

            if pushup_formula > 0.9:
                if self.direction == 0:
                    # counter += 0.5
                    self.direction = 1

            if squat_formula < 0.3:
                if self.direction == 1:
                    self.sit_counter += 1
                    self.direction = 0

            if pushup_formula < 0.4:
                if self.direction == 1:
                    self.push_counter += 1
                    self.direction = 0

            # wyświetlanie powtórzeń na obrazie
            cv2.putText(img, f"{self.sit_counter}", (20, 100), cv2.FONT_HERSHEY_DUPLEX, 4, (205, 50, 0), 5)
            cv2.putText(img, f"{self.push_counter}", (20, 200), cv2.FONT_HERSHEY_DUPLEX, 4, (0, 205, 50), 5)
        if return_value:
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()


cap = None


class WorkingScreen(Screen, BoxLayout):
        def init_qrtest(self):
            pass

        def dostart(self, *largs):
            global cap
            cap = cv2.VideoCapture(0)
            self.ids.qrcam.start(cap)

        def doexit(self):
            global cap
            self.ids.qrcam.stop()


class Calendar(Screen, Widget):
    def push_counter(self):
        current = self.ids.circle_bar.value


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyMainApp().run()
