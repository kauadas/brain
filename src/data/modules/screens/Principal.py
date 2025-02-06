from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

from data.modules.utils import BarraNavegacao, set_quadro, get_file_path

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
        canvas = json.load(open(get_file_path("configs","configs.json")))["last-five-canvas"]
        return canvas
        
    def load_quadros(self):
        self.layout.clear_widgets()
        quadros = self.get_quadros()

        for quadro in quadros:
            print(quadro)
            preview = get_file_path("quadros_images",quadro+".png")

            size = Image.open(preview).size
            width = self.height/size[1] * size[0]
            button = Button(text=quadro,size_hint=(None,1),width=width)
            button.background_normal = preview
            button.on_press = lambda x=quadro: set_quadro(x)
            self.layout.add_widget(button)

            self.layout.width += width + self.layout.spacing[0]




class JanelaPrincipal(Screen):
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
        self.title.color = (0.2,1,0.2,1)
        self.title.markup = True
        self.add_widget(self.title)

        # carrossel

        self.carrossel = Carrossel(pos_hint={"x": 0,"center_y": 0.5})
        self.add_widget(self.carrossel)

        self.on_pre_enter = self.carrossel.load_quadros


        self.bind(size=self.on_update, pos=self.on_update)

    def style(self):
        """estilo da janela."""
        pass

    def on_update(self,*args):
        self.title.font_size = self.height * 0.05

        


        
