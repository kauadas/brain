from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from kivy.graphics import *

from data.modules.utils import BarraNavegacao, configs, get_file_path, default_theme
from data.modules.widgets.color_chooser import ColorChooser
from data.modules.widgets.file_explorer import FileExplorer

from sys import path


class Theme(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme = configs.theme
        self.orientation = 'vertical'
        self.spacing = 10
        self.clrs_pickers = {}

        for key, value in self.theme.items():
            text = Label(text=key)
            self.add_widget(text)

            color = ColorChooser(size_hint=(1,1))
            color.button.background_color = self.theme["button-default"]
            color.button.background_normal = ""
            color.set_color(value)
            color.on_update()
            
            self.clrs_pickers[key] = color
            self.add_widget(color)
        


        self.button = Button(text='Salvar')
        self.button.on_press = self.save
        self.add_widget(self.button)

        self.reset = Button(text='Reset')
        self.reset.on_press = self.reset_theme
        self.add_widget(self.reset)


    def save(self):
        for key, value in self.clrs_pickers.items():
            self.theme[key] = value.color
        configs.save()

    def reset_theme(self):
        for key, value in self.clrs_pickers.items():
            self.theme[key] = default_theme[key]
            self.clrs_pickers[key].set_color(default_theme[key])
        configs.save()




def load_widget():
    popup = FileExplorer(file_chooser_options={"path": path[0]},size_hint=(0.6,0.6))
    popup.open()

    popup.on_ok = lambda popup = popup: load(popup.load_file)

def load(path_file):
    data = open(path_file).read()
    print("p",path)
    files_path = path[0]+"/data/modules/canvas_widgets"

    with open(files_path+"/"+path_file.split("/")[-1], "w") as f:
        f.write(data)
        f.close()



class ConfigsWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BarraNavegacao())
        self.style()
        self.title = Label(text='Configs', size_hint=(1, 0.05),pos_hint={'left': 0, 'top': 0.8})
        self.title.font_size = self.height
        self.title.color = configs.theme["middle-color"]
        self.add_widget(self.title)

        self.scroll = ScrollView(size_hint=(1, 0.7), do_scroll_x=False, do_scroll_y=True, always_overscroll=True)
        self.add_widget(self.scroll)

        self.layout = BoxLayout(orientation='vertical', size_hint=(1, None))
        self.layout.height = 4000
        self.scroll.add_widget(self.layout)

        self.title_theme = Label(text='Theme', size_hint=(1, 0.05),pos_hint={'left': 0, 'top': 0.8})
        self.title_theme.font_size = self.height
        self.title_theme.color = configs.theme["middle-color"]
        self.layout.add_widget(self.title_theme)

        self.theme = Theme()
        self.layout.add_widget(self.theme)

        self.load_widget = Button(text='Load widget', size_hint=(1, 0.05))
        self.load_widget.font_size = self.height
        self.load_widget.color = configs.theme["middle-color"]
        self.load_widget.on_press = load_widget
        self.layout.add_widget(self.load_widget)



        self.bind(size=self.on_update, pos=self.on_update)
        

    def style(self):
        with self.canvas.before:
            Color(*configs.theme["background-main"])
            self.background = Rectangle(pos=self.pos, size=self.size)
        
    def on_update(self,*args):
        self.background.size = self.size
        self.background.pos = self.pos