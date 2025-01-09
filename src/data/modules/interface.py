from kivy.app import App

from kivy.uix.screenmanager import ScreenManager

from .screens.Quadros import Quadros
from .screens.Principal import JanelaPrincipal


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
        janelas.add_widget(JanelaPrincipal(name='principal'))
        self.quadros = Quadros(name='quadros')
        janelas.add_widget(self.quadros)

        return janelas
    

