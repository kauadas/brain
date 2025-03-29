from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.graphics import *

from data.modules.utils import BarraNavegacao, set_canvas, get_file_path, configs

from PIL import Image
import os

import json

class Carrossel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_x = True
        self.do_scroll_y = False
        self.size_hint = (1,None)
        self.height = 200

        self.layout = StackLayout(orientation='lr-tb',pos_hint={'x':0,'y':0},size_hint=(None,1),spacing=40)
        self.layout.width = 0
        self.add_widget(self.layout)

    def get_canvas(self):
        canvas = configs.last_five_canvas
        return canvas
        
    def load_canvas(self):
        self.layout.clear_widgets()
        canvas = self.get_canvas()
        canvas_files = os.listdir(get_file_path("canvas"))
        for canva in canvas:
            if canva+".json" not in canvas_files:
                continue
            
            preview = get_file_path("canvas_images",canva+".png")

            size = Image.open(preview).size
            width = self.height/size[1] * size[0]
            button = Button(text=canva,size_hint=(None,1),width=width)
            button.background_normal = preview
            button.on_press = lambda x=canva: set_canvas(x)
            self.layout.add_widget(button)

            self.layout.width += width + self.layout.spacing[0]




class MainWindow(Screen):
    """
    janela principal do aplicativo.

    onde o usuário poderá ter uma visão geral das suas páginas e ferramentas.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        barra = BarraNavegacao()
        self.add_widget(barra)

        # titulo
        self.title = Label(text='[b]anti-acomodação[/b]', size_hint=(1, 0.05),pos_hint={'left': 0, 'top': 0.8})
        self.title.color = configs.theme["middle-color"]
        self.title.markup = True
        self.add_widget(self.title)

        # carrossel

        self.carrossel = Carrossel(pos_hint={"x": 0,"center_y": 0.5})
        self.add_widget(self.carrossel)

        self.on_pre_enter = self.carrossel.load_canvas

        self.style()
        self.bind(size=self.on_update, pos=self.on_update)

        

    def style(self):
        """estilo da janela."""
        with self.canvas.before:
            Color(*configs.theme["background-main"])
            self.rect_0 = Rectangle(pos=self.pos, size=self.size)

    def on_update(self,*args):
        self.title.font_size = self.height * 0.05

        self.rect_0.size = self.size
        self.rect_0.pos = self.pos

        


        
