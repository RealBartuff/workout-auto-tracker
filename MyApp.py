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
        self.p_direction = 0
        self.s_direction = 0
        self.event = None
        self.percent_pu = None
        self.percent_su = None

    def start(self, cap, fps=30):
        self.cap = cap
        self.event = Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        if self.event:
            Clock.unschedule(self.event)
        self.cap = None

    def update(self, dt):
        kc = KivyCamera()
        return_value, frame = self.cap.read()
        img = detector.find_pose(frame, draw=True)
        lm_list = detector.get_position(frame, False)
        if len(lm_list) != 0:
            angle1 = detector.find_angle(img, 11, 13, 15)
            angle2 = detector.find_angle(img, 23, 25, 27)# trzy punkty do określenia kąta ze wzoru mediapipe
            percent_pu = np.interp(angle1, (190, 270), (0, 100))  # zakres ruchu w procentach
            percent_su = np.interp(angle2, (170, 110), (0, 100))
            # kc.do_pups()
            # kc.do_sups()
            try:
                pushup_formula = (lm_list[13][2] - lm_list[11][2]) / (lm_list[15][2] - lm_list[13][2])
                if pushup_formula > 0.9:
                    if self.p_direction == 0:
                        # counter += 0.5
                        self.p_direction = 1
                if pushup_formula < 0.35:
                    if self.p_direction == 1:
                        self.push_counter += 1
                        self.p_direction = 0

                squat_formula = (lm_list[25][2] - lm_list[23][2]) / (lm_list[27][2] - lm_list[25][2])
                if squat_formula > 0.9:
                    if self.s_direction == 0:
                        # counter += 0.5
                        self.s_direction = 1
                if squat_formula < 0.35:
                    if self.s_direction == 1:
                        self.sit_counter += 1
                        self.s_direction = 0
            except ZeroDivisionError:
                pass

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

    # def do_pups(self):
    #
    #     if self.percent_pu == 100:
    #         if self.direction == 0:
    #             # counter += 0.5
    #             self.direction = 1
    #
    #     if self.percent_pu == 0:
    #         if self.direction == 1:
    #             self.sit_counter += 1
    #             self.direction = 0
    #
    # def do_sups(self):
    #
    #     if self.percent_su == 100:
    #         if self.direction == 0:
    #             # counter += 0.5
    #             self.direction = 1
    #
    #     if self.percent_su == 0:
    #         if self.direction == 1:
    #             self.push_counter += 1
    #             self.direction = 0


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
