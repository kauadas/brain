from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

from data.modules.utils import BarraNavegacao, set_quadro

from PIL import Image

import json

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

        self.carrossel = ScrollView(size_hint=(1, None), pos_hint={'left': 0, 'top': 0.5}, do_scroll_x=True, do_scroll_y=False,
                                    height=200)
        self.add_widget(self.carrossel)

        self.carrossel_layout = StackLayout(size_hint=(None, 1), pos_hint={'left': 0, 'top': 0}, orientation='lr-tb',width=0,
                                           spacing=20)
        
        self.carrossel_layout.bind(minimum_width=self.carrossel_layout.setter('width'))
        self.carrossel.add_widget(self.carrossel_layout)



        self.bind(size=self.on_update, pos=self.on_update)

    def style(self):
        """estilo da janela."""
        pass

    def on_update(self,*args):
        self.title.font_size = self.height * 0.05
        
    def on_pre_enter(self, *args):
        self.carrossel_layout.clear_widgets()

        with open('data/json/configs/configs.json') as f:
            configs = json.load(f)
            for quadro in configs['ultimos-5-quadros']:
                print(quadro)
                image = f"data/png/quadros/{quadro}.png"
                image_pil = Image.open(image)
                width_of_image = self.carrossel.height / image_pil.size[1] * image_pil.size[0]

                quadro = Button(size_hint=(None, 1), text=quadro, background_normal=image, background_down=image,width=width_of_image)
                self.carrossel_layout.width += width_of_image+self.carrossel_layout.spacing[0]
                
                self.carrossel_layout.add_widget(quadro)

                quadro.on_press = lambda quadro = quadro: set_quadro(quadro.text)

        
