from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window

from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget



from kivy.graphics import *

2
class Canvas(Widget):
    """Quadro onde o usuário poderá visualizar os seus widgets em uma pagina customizavel."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # scroll view do quadro para poder se movimentar pelo quadro.
        self.scroll = ScrollView(size_hint=(1,1),do_scroll_x=True,do_scroll_y=True,always_overscroll=False)
        self.page_size = 1000
        self.layout = FloatLayout(size_hint=(None,None),size=(4000,4000))
        self.scroll.add_widget(self.layout)

        self.add_widget(self.scroll)

        
        # botões para aumentar o tamanho do quadro
        self.plus_h = Button(text="+",size_hint=(None,None),
            pos_hint={'x':0.5,'top': 1})
        self.plus_h.bind(on_press=self.on_plus_height)
        
        self.add_widget(self.plus_h)

        self.plus_w = Button(text="+",size_hint=(None,None),
            pos_hint={'right': 1,'y':0.5})
        self.plus_w.bind(on_press=self.on_plus_width)
        
        self.add_widget(self.plus_w)
        

        self.style()
        self.bind(pos=self.on_update,size=self.on_update)
    


    def style(self):
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.rect_0 = Rectangle(pos=self.pos, size=self.size)
    


    def on_update(self,*args):
        self.rect_0.size = self.size
        self.rect_0.pos = self.pos

        self.scroll.size = self.size[0],self.size[1]
        self.scroll.pos = self.pos
        
        Button_w, Button_h = 400,20
        self.plus_h.size = Button_w,Button_h
        self.plus_h.center_x = self.pos[0]+self.size[0]*0.5
        self.plus_h.y = 0

        self.plus_w.size = Button_h,Button_w
        self.plus_w.center_y = self.pos[1]+self.size[1]*0.5
        self.plus_w.x = self.pos[0]+self.size[0]-20



    def on_plus_height(self,*args):
        self.layout.height += self.page_size

        # conserva a posição y de todos os widgets
        for i in self.layout.children:
            i.y += self.page_size

    def on_plus_width(self,*args):
        self.layout.width += self.page_size
            


