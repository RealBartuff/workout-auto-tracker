import kivy

kivy.require('2.0.0')

import kivy.core.text
import numpy as np
import time
import PoseModule as pm
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.base import EventLoop
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

    def start(self, cap, fps=30):
        self.cap = cap
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.cap = None

    def update(self, dt):
        counter = 0
        direction = 0
        return_value, frame = self.cap.read()
        img = detector.find_pose(frame, draw=True)
        lm_list = detector.get_position(frame, False)
        if len(lm_list) != 0:
            angle = detector.find_angle(img, 11, 13, 15)  # trzy punkty do określenia kąta ze wzoru mediapipe
            squat_formula = (lm_list[13][2] - lm_list[11][2]) / (lm_list[15][2] - lm_list[13][2])
            percent = np.interp(angle, (170, 110), (0, 100))  # zakres ruchu w procentach
            if squat_formula > 0.9:
                if direction == 0:
                    # counter += 0.5
                    direction = 1
            if squat_formula < 0.4:
                if direction == 1:
                    counter += 1
                    direction = 0
            # wyświetlanie powtórzeń na obrazie
            cv2.putText(img, f"{counter}", (50, 200), cv2.FONT_HERSHEY_DUPLEX, 5, (255, 0, 0), 5)
        if return_value:
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()

capture = None


class WorkingScreen(Screen, BoxLayout):
        def init_qrtest(self):
            pass

        def dostart(self, *largs):
            global cap
            cap = cv2.VideoCapture(0)
            self.ids.qrcam.start(cap)

        def doexit(self):
            global cap
            if cap != None:
                cap.release()
                capture = None
            EventLoop.close()


class Calendar(Screen):
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyMainApp().run()
