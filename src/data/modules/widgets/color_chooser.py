from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.graphics import *


class ColorChooserPopup(Popup):
    def __init__(self, **kwargs):
        super(ColorChooserPopup, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        self.add_widget(self.layout)

        self.red_title = Label(text="Red",size_hint=(1,0.1))
        self.layout.add_widget(self.red_title)
        self.red = Slider(min=0,max=255)
        self.layout.add_widget(self.red)

        self.green_title = Label(text="Green",size_hint=(1,0.1))        
        self.layout.add_widget(self.green_title)

        self.green = Slider(min=0,max=255)
        self.layout.add_widget(self.green)

        self.blue_title = Label(text="Blue",size_hint=(1,0.1))        
        self.layout.add_widget(self.blue_title)
        self.blue = Slider(min=0,max=255)
        self.layout.add_widget(self.blue)

        self.button = Button(text="OK",size_hint=(1,0.1))
        self.layout.add_widget(self.button)

        self.button.on_press = self.dismiss

    def get_color(self):
        return [self.red.value/255,self.green.value/255,self.blue.value/255]
    
    def set_color(self,color):
        self.red.value = color[0]*255
        self.green.value = color[1]*255
        self.blue.value = color[2]*255

class ColorChooser(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color_chooser = ColorChooserPopup(size_hint=(0.5,0.5))
        self.color = [0,0,0]

        self.style()

        self.button = Button(text="Choose Color",size_hint=(None,1))
        self.button.on_press = self.color_chooser.open
        self.add_widget(self.button)

        self.color_chooser.bind(on_dismiss=self.on_dismiss)
        self.bind(size=self.on_update, pos=self.on_update)

        self.on_update()

        

    def on_dismiss(self,*args):
        self.color = self.color_chooser.get_color()
        self.on_update()

    def style(self):
        with self.canvas.after:
            Color(1,1,1,1)
            self.rect_0 = Rectangle(pos=self.pos, size=self.size)
            self.color_graphic = Color(*self.color)
            self.rect_1 = Rectangle(pos=self.pos, size=self.size)
            
    def on_update(self,*args):
        self.color_graphic.rgba = self.color+[1]

        size_1 = 0.6
        size_0 = 0.4
        
        self.rect_0.size = self.size[0]*0.5,self.size[1]
        self.rect_0.pos = self.pos[0]+self.size[0]*0.5,self.pos[1]

        self.rect_1.size = self.size[0]*0.4,self.size[1]*0.9
        self.rect_1.pos = self.pos[0]+self.size[0]*0.55,self.pos[1]+self.size[1]*0.05

        self.button.width = self.size[0]*0.5

    def set_color(self,color):
        self.color = color
        self.color_chooser.set_color(color)
        self.on_update()