from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from kivy.graphics import *

from ..widgets.quadro import Quadro
from ..utils import types, BarraNavegacao


import json
import os


def salvar_quadro(filename: str, quadro):
    """
    salva o quadro em um arquivo json

    filename: str
    quadro: Quadro
    """

    data = {"widgets": {},
            "size": quadro.layout.size}
    for i,item in enumerate(quadro.layout.children):
        
        data["widgets"][str(type(item).__name__)+str(i)] = item.to_json()

    with open("data/json/quadros/"+filename+".json",'w') as file:
        json.dump(data,file,indent=4)

    

def load_quadro(filename: str,quadro: Quadro):
    """
    carrega o quadro de um arquivo json
    """


    with open("data/json/quadros/"+filename+".json") as file:
        data = json.load(file)

    quadro.layout.clear_widgets()

    for i in data["widgets"]:
        print(data["widgets"][i])
        item = types[data["widgets"][i]['type']](size_hint=(None,None))
        item.from_json(data["widgets"][i])
        quadro.layout.add_widget(item)
        print(item)

    quadro.layout.size = data["size"]
    

class Quadros(Screen):
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
        self.buttons = BoxLayout(orientation='horizontal',size_hint=(1,0.05))
        self.supra_layout.add_widget(self.buttons)

        self.list_buttons = {"Salvar": self.save,"Carregar": self.load,
                             "adicionar": self.add_item,"limpar": self.clear,
                             "centralizar": self.go_center}
        
        for text,function in self.list_buttons.items():
            button = Button(text=text,size_hint=(0.2,1))
            button.on_press = function
            self.buttons.add_widget(button)

        
        
        # quadro
        self.quadro = Quadro()
        self.supra_layout.add_widget(self.quadro)

        
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
        button.on_press = lambda: salvar_quadro(text_input.text,self.quadro)
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

        quadros = os.listdir("data/json/quadros/")
        for quadro in quadros:
            quadro = quadro.replace(".json","")
            button = Button(text=quadro,size_hint=(1,None),height=100)
            button.on_press = lambda x=quadro: load_quadro(x,self.quadro)
            scroll_layout.add_widget(button)

        print(quadro)
    
        button_close = Button(text="close",size_hint=(1,0.1))
        button_close.on_press = popup.dismiss
        layout.add_widget(button_close)
        
        popup.open()

    def clear(self,*args):
        """limpa o quadro atual e reseta o tamanho."""
        
        self.quadro.layout.clear_widgets()
        self.quadro.layout.size = (4000,4000)

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
            pos = (self.quadro.layout.width*0.4,self.quadro.layout.height*0.4)
            button.on_press = lambda x=obj: self.quadro.layout.add_widget(x(size_hint=(None,None),size=(400,400),pos=pos))
            scroll_layout.add_widget(button)
    
        button_close = Button(text="close",size_hint=(1,0.1))
        button_close.on_press = popup.dismiss
        layout.add_widget(button_close)

        popup.open()
        
    def go_center(self,*args):
        """centraliza o quadro na tela."""
        
        self.quadro.scroll.scroll_x = 0.5
        self.quadro.scroll.scroll_y = 0.5
