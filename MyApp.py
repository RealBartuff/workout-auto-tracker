import kivy
import sys
import Exercises

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Design(GridLayout):
    def __init__(self, **kwargs):
        super(Design, self).__init__(**kwargs)
        self.cols = 1

        self.start_btn = Button(text="START TRAINING",
                                font_size=20
                                )
        self.start_btn.bind(on_press=self.start_workout)
        self.add_widget(self.start_btn)
        self.stop_btn = Button(text="STOP",
                               font_size=20
                               )
        self.stop_btn.bind(on_press=self.pause)
        self.add_widget(self.stop_btn)

    def start_workout(self, instance):
        print("Running...")
        Exercises.run_program()

    def pause(self, instance):
        while True:
            break


class MyApp(App):
    def build(self):
        return Design()


if __name__ == '__main__':
    MyApp().run()