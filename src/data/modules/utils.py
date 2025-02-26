from .widgets.floatwidget import FloatWidget
from .canvas_widgets import types
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *

from PIL import Image

import os
from sys import path
import json

class BarraNavegacao(BoxLayout):
    """
    barra de navegação do aplicativo.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, 0.07)
        self.pos_hint = {'left': 0, 'top': 1}
        self.spacing = 10


        self.style()
        self.bind(size=self.on_update, pos=self.on_update)

        self.on_update()

        self.button('Principal', 'principal')

        self.button('Canvas', 'canvas')

        self.button('Configs', 'configs')

    def style(self):
        """cria o estilo da barra de navegação."""
        pass

    def on_update(self, *args):
        pass

    def button(self, text, janela):
        button = Button(text=text)
        button.background_color = configs.theme["button-default"]
        button.background_normal = ""
        button.on_press = lambda: self.go_to(janela)
        self.add_widget(button)
        return button
        

    def go_to(self,name,*args):
        App.get_running_app().root.current = name




root = path[0]
paths = {
    "images": root+"/data/images/",
    "canvas_images": root+"/data/images/canvas/",
    "json": root+"/data/json/",
    "canvas": root+"/data/json/saves/",
    "configs": root+"/data/json/configs/",
    
}



def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return [i/255 for i in tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))]


def create_config():
    """cria o arquivo de config do aplicativo"""

    # data do arquivo config.
    config_data = {"last-five-canvas":[]}

    with open(config_path,"w") as file:
        json.dump(config_data,file,indent=4)
        file.close()

def get_file_path(path: str, filename: str = ""):
    return paths[path] + "/" + filename



def generate_paths():
    for path in paths.values():
        print(path)
        print(os.path.exists(path))
        if not os.path.exists(path):
            print("creating...")
            os.makedirs(path)

config_path = get_file_path("configs","configs.json")

default_theme = {
        "middle-color": [
            0.9333333333333333,
            0.8901960784313725,
            0.6784313725490196
        ],
        "background-main": [
            0.28627450980392155,
            0.3333333333333333,
            0.34901960784313724
        ],
        "background-canvas": [
            0.3568627450980392,
            0.43137254901960786,
            0.4549019607843137
        ],
        "floatlayout-bar": [
            0.7607843137254902,
            0.6941176470588235,
            0.611764705882353
        ],
        "button-default": [
            0.6705882352941176,
            0.611764705882353,
            0.5411764705882353
        ],
        "button-default-pressed": [
            0.7607843137254902,
            0.6941176470588235,
            0.611764705882353
        ],
        "text-color": [
            0.0,
            0.0,
            0.0
        ]
    }

class Configs:
    def __init__(self):
        self.last_five_canvas = []

        self.theme = default_theme

        self.load()

    def load(self):

        if not os.path.isfile(config_path):
            self.save()

        with open(config_path) as file:
            data = json.load(file)
            file.close()

        self.last_five_canvas = data["last-five-canvas"]
        self.theme = data["theme"]


    def save(self):
        data = {
            "last-five-canvas": self.last_five_canvas,
            "theme": self.theme
        }

        if not os.path.isdir(get_file_path("configs")):
            os.makedirs(get_file_path("configs"))

        with open(config_path,"w") as file:
            json.dump(data,file,indent=4)
            file.close()

configs = Configs()


def delete_canvas(name: str):
    """
    deleta um canva
    """
    
    os.remove(get_file_path("canvas",name+".json"))
    os.remove(get_file_path("canvas_images",name+".png"))

    if name in configs.last_five_canvas:
        configs.last_five_canvas.remove(name)
        configs.save()
    

def add_canvas_to_list(name: str):
    """
    adiciona um canva ao list de canvas recentes
    """

    #create_config()
    print(name)
    last_canvas = configs.last_five_canvas

    if name in last_canvas:
        print("removing", name)
        last_canvas.remove(name)

    last_canvas.insert(0,name)

    if len(last_canvas) > 5:
        print("removing the last element of list.")
        last_canvas.pop()

    configs.save()

def canvas_to_image(filename: str,canvas):
    """
    cria uma imagem com o canva
    """
    
    path = get_file_path("canvas_images",filename+".png")

    canvas.export_to_png(path)

    image = Image.open(path)
    image = image.crop((0,0,800,545))

    image.save(path)


def save_canvas(filename: str, canvas):
    """
    salva o canva em um arquivo json

    filename: str
    canva: Canva
    """

    data = {"widgets": {},
            "size": canvas.layout.size,
            "pos": [canvas.scroll.scroll_x, canvas.scroll.scroll_y]}
    
    for i,item in enumerate(canvas.layout.children):
        
        data["widgets"][str(type(item).__name__)+str(i)] = item.to_json()

    with open(get_file_path("canvas",filename+".json"),'w') as file:
        json.dump(data,file,indent=4)

    add_canvas_to_list(filename)

    canvas_to_image(filename,canvas)

import json

def load_canvas(filename: str,canvas):
    """
    carrega o canva de um arquivo json
    """
    path = get_file_path("canvas",filename+".json")
    with open(path) as file:
        data = json.load(file)

    canvas.layout.clear_widgets()

    for i in data["widgets"]:
        print("loading",data["widgets"][i])
        item = types[data["widgets"][i]['type']](size_hint=(None,None),theme = configs.theme)
        item.from_json(data["widgets"][i])
        canvas.layout.add_widget(item)
        print(item)

    canvas.layout.size = data["size"]

    add_canvas_to_list(filename)

    canvas.scroll.scroll_x = data["pos"][0]
    canvas.scroll.scroll_y = data["pos"][1]
    


def set_canvas(canvas_name: str):
    """
    seta o canva atual.

    """

    window = App.get_running_app().canvas_window
    canvas = window.canvas_layout

    load_canvas(canvas_name,canvas)

    App.get_running_app().root.current = window.name


class ErrorPopup(Popup):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = BoxLayout(orientation="vertical")
        self.add_widget(self.box)
        self.label = Label(text=text)
        self.box.add_widget(self.label)
        self.title = "Error"
        self.size_hint = (0.4,0.4)
        self.button = Button(text="OK")
        self.button.on_press = self.dismiss
        self.box.add_widget(self.button)

        self.open()

