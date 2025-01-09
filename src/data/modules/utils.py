from .floatwidget import FloatWidget
from data.modules.widgets.markdown import Markdown
from data.modules.widgets.checklist import Checklist


types = {
        'floatwidget': FloatWidget,
        'markdown': Markdown,
        'checklist': Checklist
    }


from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *

class BarraNavegacao(BoxLayout):
    """
    barra de navegação do aplicativo.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, 0.05)
        self.pos_hint = {'left': 0, 'top': 1}


        self.style()
        self.bind(size=self.on_update, pos=self.on_update)

        self.on_update()

        Principal = self.button('Principal', 'principal')

        Quadros = self.button('Quadros', 'quadros')
        
        

    def style(self):
        """cria o estilo da barra de navegação."""
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect_0 = Rectangle(pos=self.pos, size=self.size)

    def on_update(self, *args):
        self.rect_0.size = self.size
        self.rect_0.pos = self.pos

    def button(self, text, janela):
        button = Button(text=text)
        button.on_press = lambda: self.go_to(janela)
        self.add_widget(button)
        return button
        

    def go_to(self,name,*args):
        App.get_running_app().root.current = name

import os

def add_quadro_to_list(quadro_name: str):
    """
    adiciona um quadro ao list de quadros recentes
    """

    with open("data/json/configs/configs.json") as file:
        data = json.load(file)
        file.close()

    if quadro_name in data["ultimos-5-quadros"]:
        data["ultimos-5-quadros"].remove(quadro_name)

    data["ultimos-5-quadros"].insert(0,quadro_name)

    if len(data["ultimos-5-quadros"]) > 5:
        data["ultimos-5-quadros"].pop()

    with open("data/json/configs/configs.json","w") as file:
        json.dump(data,file,indent=4)
        file.close()

def quadro_para_imagem(filename: str,quadro):
    """
    cria uma imagem com o quadro
    """
    
    if not os.path.exists("data/png/"):
        os.mkdir("data/png/")
    
    if not os.path.exists("data/png/quadros"):
        os.mkdir("data/png/quadros")

    quadro.export_to_png("data/png/quadros/"+filename+".png")


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

    add_quadro_to_list(filename)

    quadro_para_imagem(filename,quadro)

    

import json

def load_quadro(filename: str,quadro):
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

    add_quadro_to_list(filename)

    quadro.scroll.scroll_x = 0.5
    quadro.scroll.scroll_y = 0.5
    


def set_quadro(quadro: str):
    """
    seta o quadro atual.

    """

    quadros = App.get_running_app().quadros
    quadro_obj =quadros.quadro

    load_quadro(quadro,quadro_obj)

    App.get_running_app().root.current = quadros.name
