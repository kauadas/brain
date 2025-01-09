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


