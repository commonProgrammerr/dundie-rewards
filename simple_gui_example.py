from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class KivySum(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1

        return self.window


KivySum().run()
