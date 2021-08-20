import kivy
import sys
import Exercises

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class WindowManager(ScreenManager):
    pass


class Menu(Screen, Widget):
    def start_btn(self):
        print("Running...")
        Exercises.run_program()

    def stop_btn(self):
        print("Stop")
        return


class WorkingScreen(Screen):
    pass


class Calendar(Screen):
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyMainApp().run()