from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from kivy.graphics import *

from ..widgets.canvas import Canvas
from ..utils import types, BarraNavegacao, load_canvas, save_canvas, get_file_path, configs

import os



class buttons(BoxLayout):
    def __init__(self,parent_widget, **kwargs):
        super().__init__(**kwargs)
        self.parent_widget = parent_widget
        self.orientation = 'horizontal'

        self.list_buttons = {"Salvar": self.parent_widget.save,"Carregar": self.parent_widget.load,
                             "adicionar": self.parent_widget.add_item,"limpar": self.parent_widget.clear,
                             "centralizar": self.parent_widget.go_center}

        for text,function in self.list_buttons.items():
            button = Button(text=text,size_hint=(1,1))
            button.on_press = function
            button.background_color = configs.theme["middle-color"]
            button.background_normal = ""
            button.color = configs.theme["text-color"]
            self.add_widget(button)


class CanvasWindow(Screen):
    """
    quadro onde o usuário poderá visualizar os seus widgets em uma pagina customizavel.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # layout onde todas as coisas vão ficar
        self.supra_layout = BoxLayout(orientation='vertical')
        self.add_widget(self.supra_layout)

        # barra de navegação
        barra = BarraNavegacao()
        self.supra_layout.add_widget(barra)

        # botões
        self.buttons = buttons(self,size_hint=(1,0.05))
        self.supra_layout.add_widget(self.buttons)
        
        
        # quadro

        self.canvas_layout = Canvas(theme=configs.theme)
        self.supra_layout.add_widget(self.canvas_layout)

        
    def save(self,*args):
        """abre um pop-up onde o usuário pode salvar o quadro atual.
        o usuário deve escolher um nome para o arquivo json e clicar em salvar e depois em close.
        """
        popup = Popup(title="Salvar",size_hint=(None,None),size=(400,400))
        layout = BoxLayout(orientation='vertical')
        popup.add_widget(layout)

        text_input = TextInput(multiline=False,size_hint=(1,0.1))
        layout.add_widget(text_input)

        button = Button(text="salvar",size_hint=(1,0.1))
        button.on_press = lambda: save_canvas(text_input.text,self.canvas_layout)
        layout.add_widget(button)

        button_close = Button(text="close",size_hint=(1,0.1))
        button_close.on_press = popup.dismiss
        layout.add_widget(button_close)

        
        popup.open()


    def load(self,*args):
        """
        abre um pop-up onde o usuário pode escolher um quadro para carregar.
        a função limpara o quadro atual e depois carrega o quadro escolhido.
        """
        
        popup = Popup(title="Carregar",size_hint=(None,None),size=(400,400))
        
        layout = BoxLayout(orientation='vertical')
        popup.add_widget(layout)


        scroll = ScrollView(size_hint=(1,1),do_scroll_x=False,do_scroll_y=True,always_overscroll=True)
        scroll_layout = StackLayout(orientation='lr-tb',size_hint=(1,None))
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        scroll.add_widget(scroll_layout)
        layout.add_widget(scroll)

        canvas = os.listdir(get_file_path("canvas"))
        for canva in canvas:
            canva = canva.replace(".json","")
            button = Button(text=canva,size_hint=(1,None),height=100)
            button.on_press = lambda x=canva: load_canvas(x,self.canvas_layout)
            scroll_layout.add_widget(button)

        print(canvas)
    
        button_close = Button(text="close",size_hint=(1,0.1))
        button_close.on_press = popup.dismiss
        layout.add_widget(button_close)
        
        popup.open()

    def clear(self,*args):
        """limpa o quadro atual e reseta o tamanho."""
        
        self.canvas_layout.layout.clear_widgets()
        self.canvas_layout.layout.size = (4000,4000)
        self.go_center()

    def add_item(self,*args):
        """abre um pop-up onde o usuário pode escolher um widget para adicionar ao quadro."""
        
        popup = Popup(title="add item",size_hint=(None,None),size=(400,400))
        layout = BoxLayout(orientation='vertical')
        popup.add_widget(layout)


        scroll = ScrollView(size_hint=(1,1),do_scroll_x=False,do_scroll_y=True,always_overscroll=True)
        scroll_layout = StackLayout(orientation='lr-tb',size_hint=(1,None))
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        scroll.add_widget(scroll_layout)
        layout.add_widget(scroll)

        for type,obj in types.items():
            button = Button(text=type,size_hint=(1,None),height=100)
            pos = (self.canvas_layout.layout.width*0.4,self.canvas_layout.layout.height*0.4)
            button.on_press = lambda x=obj: self.canvas_layout.layout.add_widget(x(theme=configs.theme,size_hint=(None,None),size=(400,400),pos=pos))
            scroll_layout.add_widget(button)
    
        button_close = Button(text="close",size_hint=(1,0.1))
        button_close.on_press = popup.dismiss
        layout.add_widget(button_close)

        popup.open()
        
    def go_center(self,*args):
        """centraliza o quadro na tela."""
        
        self.canvas_layout.scroll.scroll_x = 0.5
        self.canvas_layout.scroll.scroll_y = 0.5
