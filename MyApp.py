import sys

import kivy

kivy.require('2.0.0')

import kivy.core.text
import numpy as np
import time
from datetime import date
import PoseModule as pm
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
import sqlite3


detector = pm.PoseDetector()
conn = sqlite3.connect("record_trackDB.db")
c = conn.cursor()


class WindowManager(ScreenManager):
    pass


class Menu(Screen):
    def end(self):
        c.close()
        conn.close()
        sys.exit(MyMainApp)


class Exercises:
    def __init__(self, **kwargs):
        super(Exercises, self).__init__(**kwargs)
        self.counter = 0
        self.direction = 0


class PushUps(Exercises):
    def do_rep(self, lm_list, img):
        pushup_formula = (lm_list[13][2] - lm_list[11][2]) / (lm_list[15][2] - lm_list[13][2])
        angle1 = detector.find_angle(img, 11, 13, 15)
        if pushup_formula > 0.9:
            if self.direction == 0:
                self.direction = 1
                c.execute("UPDATE RecordOne SET Pushups=Pushups+? where Date=?", (self.counter / 2, date.today(),))

        if pushup_formula < 0.35:
            if self.direction == 1:
                self.counter += 1
                self.direction = 0
        conn.commit()

    def show_reps(self, img):
        cv2.putText(img, f"{self.counter}", (20, 200), cv2.FONT_HERSHEY_DUPLEX, 4, (0, 205, 150), 5)


class SitUps(Exercises):
    def do_rep(self, lm_list, img):
        squat_formula = (lm_list[25][2] - lm_list[23][2]) / (lm_list[27][2] - lm_list[25][2])
        angle2 = detector.find_angle(img, 23, 25, 27)
        try:
            if squat_formula > 0.9:
                if self.direction == 0:
                    self.direction = 1
                    c.execute("UPDATE RecordOne SET Situps=Situps+? where Date=?", (self.counter / 2, date.today(), ))

            if squat_formula < 0.35:
                if self.direction == 1:
                    self.counter += 1
                    self.direction = 0
        except ZeroDivisionError:
            pass
        conn.commit()

    def show_reps(self, img):
        cv2.putText(img, f"{self.counter}", (20, 100), cv2.FONT_HERSHEY_DUPLEX, 4, (205, 150, 0), 5)


class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.cap = None
        self.event = None
        self.push_ups = PushUps()
        self.sit_ups = SitUps()

    def start(self, cap, fps=30):
        self.cap = cap
        self.start_day()
        self.event = Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        if self.event:
            Clock.unschedule(self.event)
        self.cap = None

    def start_day(self):
        c.execute('CREATE TABLE IF NOT EXISTS RecordONE (Pushups INTEGER, Situps INTEGER, Date TEXT)')
        today = date.today()
        c.execute("select * from RecordOne where Date=?", (today, ))
        if not len(c.fetchall()):
            c.execute("INSERT INTO RecordONE (Pushups, Situps, Date) VALUES(?, ?, ?)", (0, 0, today))

    def update(self, dt):
        return_value, frame = self.cap.read()
        img = detector.find_pose(frame, draw=True)
        lm_list = detector.get_position(frame, False)
        if lm_list and lm_list[27][3] > 0.7:
            try:
                self.sit_ups.do_rep(lm_list, img)
                self.sit_ups.show_reps(img)
            except ZeroDivisionError:
                pass

        if lm_list and lm_list[15][3] > 0.9:
            try:
                self.push_ups.do_rep(lm_list, img)
                self.push_ups.show_reps(img)
            except ZeroDivisionError:
                pass

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
        def dostart(self, *largs):
            global cap
            cap = cv2.VideoCapture(0)
            self.ids.qrcam.start(cap)

        def doexit(self):
            global cap
            self.ids.qrcam.stop()


class P(FloatLayout):
    def set_goals(self):
        pass


class Calendar(Screen):
    message_p = StringProperty(str(0))
    message_s = StringProperty(str(0))
    def get_pups(self):
        c.execute('SELECT Pushups FROM RecordONE where date=?', (date.today(), ))
        pups = c.fetchall()[-1][0]
        return pups

    def get_sits(self):
        c.execute('SELECT Situps FROM RecordONE where date=?', (date.today(),))
        sits = c.fetchall()[-1][0]
        return sits

    def show_popup(self):
        show = P()
        popup_window = Popup(title="Daily Workout Goals", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyMainApp().run()
