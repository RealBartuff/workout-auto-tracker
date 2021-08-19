import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button


class MyApp(App):

    def build(self):
        parent = Widget()
        startbtn = Button(text="START \nWORKOUT", size=(100, 100), pos_hint={"x":1, "y":1, "left":1, "right":1,
                                                                             "center_x":5, "center_y":5, "top":1,
                                                                             "bottom":1})
        parent.add_widget(startbtn)
        return parent


if __name__ == '__main__':
    MyApp().run()