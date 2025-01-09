from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from data.modules.utils import BarraNavegacao

class JanelaPrincipal(Screen):
    """
    janela principal do aplicativo.

    onde o usuário poderá ter uma visão geral das suas páginas e ferramentas.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        barra = BarraNavegacao()
        self.add_widget(barra)

        self.title = Label(text='[b]anti-acomodação[/b]', size_hint=(1, 0.05),pos_hint={'left': 0, 'top': 0.8})
        self.title.color = (0.2,1,0.2,1)
        self.title.markup = True
        self.add_widget(self.title)

        self.bind(size=self.on_update, pos=self.on_update)

    def style(self):
        """estilo da janela."""
        pass

    def on_update(self,*args):
        self.title.font_size = self.height * 0.05
        
