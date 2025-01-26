from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from .code_widget import Code, ErrorPopup



class Bar(StackLayout):
    def __init__(self,parent_widget, **kwargs):
        super().__init__(**kwargs)
        self.parent_widget = parent_widget
        self.orientation = 'lr-tb'
        self.size_hint = (None,None)
        self.size_base = [1,0.1]
        size_button = 1/6
        self.move_center = [3.5*size_button,1+size_button/2]

        self.title = Label(text="floatwidget",size_hint=(2*size_button,1))
        self.add_widget(self.title)

        Button_remove = Button(text='X',size_hint=(size_button,1))
        Button_remove.on_press = self.parent_widget.on_remove

        Button_move = Button(text='>',size_hint=(size_button,1))
        Button_move.on_press = lambda *args : self.parent_widget.set_move(True)
        Button_move.on_release = lambda *args : self.parent_widget.set_move(False)

        Button_resize = Button(text='|',size_hint=(size_button,1))
        Button_resize.on_press = self.parent_widget.on_start_resize
        Button_resize.on_release = self.parent_widget.on_stop_resize

        Button_code = Button(text='code',size_hint=(size_button,1))
        Button_code.on_press = self.parent_widget.code.open

        self.add_widget(Button_remove)
        self.add_widget(Button_move)
        self.add_widget(Button_resize)
        self.add_widget(Button_code)
        


    def update(self):
        self.pos = self.parent_widget.pos[0], self.parent_widget.pos[1]+self.parent_widget.height

        self.size = [x*i for x,i in zip(self.parent_widget.size,self.size_base)]
        
       
class CodeUi(Code):
    def __init__(self, parent_widget,**kwargs):
        super().__init__(**kwargs)
        self.parent_widget = parent_widget
        
        self.on_dismiss = self.start_event_code

    def start_event_code(self):
        print("set event",self.code)
        self.parent_widget.event = Clock.schedule_interval(self.run_code, self.time_trigger)

    def open(self):
        super().open()
        if self.parent_widget.event:
            self.parent_widget.event.cancel()

        

    def run_code(self,*args):
        
        try:
            exec_globals = {"self":self.parent_widget}
            exec_locals = {}
            exec(self.code,exec_globals,exec_locals)

        except Exception as e:
            ErrorPopup("Error running code: "+str(e))
            self.stop_event()

    def stop_event(self):
        if self.parent_widget.event:
            self.parent_widget.event.cancel()

            self.parent_widget.event = None


class FloatWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # widgets
        self.code = CodeUi(self)

        self.barra = Bar(self)

        self.content = FloatLayout(pos=self.pos)

        self.content.add_widget(self.barra)
        self.add_widget(self.content)
        
        # vars
        self.move = False
        self.resize = False

        # functions calls

        self.style()
        

        self.bind(size=self.on_update, pos=self.on_update)
        self.on_update()

        # executar codigo 
        self.event = None

    def style(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect_0 = Rectangle(pos=self.pos, size=self.size)
            Color(0.2,1,0.2,1)
            self.rect_1 = Rectangle(pos=self.barra.pos, size=self.barra.size)

    def on_update(self, *args):

        self.barra.update()
        self.content.pos = self.pos
        self.content.size = self.size
        self.style()

        

    def set_move(self,value: bool,*args):
        self.move = value

    def on_touch_move(self, touch):
        
        # movimentação
        if self.move:
            x,y = touch.pos

            move_center = self.barra.move_center
            x,y = x-self.size[0]*move_center[0],y-self.size[1]*move_center[1]

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
        return {"type":"floatwidget","pos":self.pos,"size":self.size,"code": (self.code.code,self.code.time_trigger)}
    
    def from_json(self,data):
        self.pos = data["pos"]
        self.size = data["size"]
        self.code.code = data["code"][0]
        self.code.code_input.text = data["code"][0]
        self.code.time_trigger = data["code"][1]
        self.code.time_input.text = str(data["code"][1])
        self.code.start_event_code()
    
    def set_title(self,title):
        self.barra.title.text = title


