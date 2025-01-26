

from kivy.app import App
from kivy.uix.button import Button

from kivy.uix.floatlayout import FloatLayout

from kivy.graphics import Color, Line

import math

class Button0(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points = [self.center]
        self.move = False
        self.line = None

    def on_press(self, *args):
        self.move = True
        self.points = [self.center]

    def on_release(self, *args):
        self.move = False

        


    def on_touch_move(self, touch):
        if self.move:
            x,y = touch.pos

            x_1, y_1 = self.points[-1]
            print(self.points)
            print(x,y,x_1,y_1)
            

            vetor = {"x": abs(x - x_1), "y": abs(y - y_1)}
            print(vetor)
            angle = max(vetor,key=vetor.get)
            print(angle)
            
            if math.dist((x,y),(x_1,y_1)) > 100:
                if angle == "x":
                    self.points.append((x,y_1))

                else:
                    self.points.append((x_1,y))

            print(angle,self.points[-1])

        if self.line:
            self.parent.canvas.remove(self.line)

        self.line = Line(points=self.points, width=10, color=(1, 0, 0, 1))
        self.parent.canvas.add(self.line)


class App(App):
    def build(self):
        w = FloatLayout()

        b = Button0(pos_hint={"x": 0, "center_y": 0.5},size=(100,100),size_hint=(None,None))
        w.add_widget(b)

        return w
    

App().run()