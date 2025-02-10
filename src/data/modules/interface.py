from kivy.app import App

from kivy.uix.screenmanager import ScreenManager

from .screens.Canvas_window import CanvasWindow
from .screens.Principal import MainWindow


class Janelas(ScreenManager):
    """
    gerenciador de janelas.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

class Aplicativo(App):
    """
    classe principal do aplicativo."""
    def build(self):
        self.title = "anti-acomodação"
        janelas = Janelas()
        janelas.add_widget(MainWindow(name='principal'))
        self.canvas_window = CanvasWindow(name='canvas')
        janelas.add_widget(self.canvas_window)

        return janelas
    


