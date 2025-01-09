from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window

from kivy.graphics import Color, Rectangle

class FloatWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = Label(text="floatwidget",size_hint=(2/5,1))
        

        self.barra = StackLayout(orientation='lr-tb',pos=(self.pos[0],self.top),size_hint=(1,0.1))
        self.add_widget(self.barra)
        Button_remove = Button(text='X',size_hint=(1/5,1))
        Button_remove.on_press = self.on_remove

        Button_move = Button(text='>',size_hint=(1/5,1))
        Button_move.on_press = self.on_move
        Button_move.on_release = self.on_stop

        button_resize = Button(text='|',size_hint=(1/5,1),pos=(self.right,self.y))
        button_resize.on_press = self.on_start_resize
        button_resize.on_release = self.on_stop_resize

        self.barra.add_widget(Button_remove)
        self.barra.add_widget(Button_move)

        self.barra.add_widget(self.title)
        self.barra.add_widget(button_resize)

        self.content = FloatLayout(pos=self.pos)

        self.add_widget(self.content)
        
        self.style()

        self.bind(size=self.on_update, pos=self.on_update)
        self.on_update()

        self.move = False
        self.resize = False

    def style(self):
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect_0 = Rectangle(pos=self.pos, size=self.size)
            Color(0.2,1,0.2,1)
            self.rect_1 = Rectangle(pos=self.barra.pos, size=self.barra.size)

    def on_update(self, *args):
        W_size = Window.size
        self.barra.size = self.size[0],self.size[1]*0.1
        self.barra.pos = self.x,self.y+self.size[1]
        self.content.size = self.size[0],self.size[1]*0.9
        self.content.pos = self.pos

        self.rect_0.size = self.content.size
        self.rect_0.pos = self.content.pos

        self.rect_1.size = self.barra.size
        self.rect_1.pos = self.barra.pos

        

    def on_move(self, *args):
        self.move = True

    def on_stop(self, *args):
        self.move = False

    def on_touch_move(self, touch):
        W_size = Window.size
        if self.move:
            x,y = touch.pos
            x,y = x-self.size[0]*1.5/4,y-self.height*1.05
            final_x, final_y = self.x,self.y
            if x > self.parent.x and x+self.size[0] < self.parent.right:
                final_x = x

            if y > self.parent.y and y+self.size[1]*1.05 < self.parent.top:
                final_y = y

            self.pos = final_x,final_y

            

        elif self.resize:
            x,y = touch.pos
            w,h = x-self.x,y-self.y

            final_w, final_h = self.width,self.height
            if w > 100:
                final_w = w

            if h > 100:
                final_h = h

            self.size = final_w,final_h


    def on_touch_up(self, touch):
        if self.move:
            self.move = False
        elif self.resize:
            self.resize = False
            
    def on_remove(self, *args):
        self.parent.remove_widget(self)

    def on_start_resize(self,*args):
        self.resize = True

    def on_stop_resize(self,*args):    
        self.resize = False

    def to_json(self):
        return {"type":"floatwidget","pos":self.pos,"size":self.size}
    
    def from_json(self,data):
        self.pos = data["pos"]
        self.size = data["size"]
    
    def set_title(self,title):
        self.title.text = title