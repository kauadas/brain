from ..widgets.floatwidget import FloatWidget

from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from kivy.uix.widget import Widget



from kivy.graphics import Color, Rectangle

class ChecklistItem(Widget):
    def __init__(self,theme: dict,text: str, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.theme = theme

        self.check = CheckBox()
        self.check.size_hint = (None, None)
        self.label = Label(text=text,color=(0,0,0,1))
        self.label.size_hint = (None, None)
        self.remove = Button(text='X',size_hint=(None, None))
        self.remove.on_press = self.remove_item
        self.add_widget(self.check)
        self.add_widget(self.label)
        self.add_widget(self.remove)

        self.bind(size=self.on_update, pos=self.on_update)
        self.style()

    def on_update(self, *args):
        
        self.check.size = (self.height, self.height)
        self.check.pos = self.pos

        self.check_rect.size = (self.height, self.height)
        self.check_rect.pos = self.pos
        
        self.label.size = (self.width - self.check.width - self.height, self.height)
        self.label.pos = (self.check.right, self.pos[1])

        self.remove.size = (self.height, self.height)
        self.remove.pos = (self.label.right, self.pos[1])
        
        self.rect_0.size = self.size
        self.rect_0.pos = self.pos

    def style(self):
        with self.canvas.before:
            Color(*self.theme["button-floatlayout"])
            self.rect_0 = Rectangle(pos=self.pos, size=self.size)
            Color(*self.theme["middle-color"])
            self.check_rect = Rectangle(pos=self.pos, size=(self.height, self.height))

    def remove_item(self, *args):
        self.parent.remove_widget(self)


class Checklist(FloatWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Checklist")

        self.scroll = ScrollView(pos_hint={'x':0,'y':0.1},size_hint=(1,0.9),do_scroll_x=False,do_scroll_y=True,always_overscroll=True)
        self.content.add_widget(self.scroll)
        self.layout = StackLayout(orientation='lr-tb',pos_hint={'x':0,'y':0},size_hint=(1,None),spacing = [0,10])
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.scroll.add_widget(self.layout)

        self.itens = {}

        self.buttons = BoxLayout(orientation='horizontal',size_hint=(1,0.1),pos_hint={'x':0,'y':0})
        add_button = Button(text="+",size_hint=(1/3,1))
        add_button.background_color = self.theme["button-floatlayout"]
        add_button.background_normal = ""
        add_button.on_press = self.add_item_pop_up
        self.buttons.add_widget(add_button)

        self.content.add_widget(self.buttons)

        reset_button = Button(text="reset",size_hint=(1/3,1))
        reset_button.background_color = self.theme["button-floatlayout"]
        reset_button.background_normal = ""
        reset_button.on_press = self.reset_itens
        self.buttons.add_widget(reset_button)

    def add_item(self, text: str):
        if not text in self.itens:
            item = ChecklistItem(text=text,size_hint=(1,None),height=50,theme=self.theme)
            self.itens[text] = item
            self.layout.add_widget(item)


    def add_item_pop_up(self, *args):
        pop = Popup(title="Add item",size_hint=(None,None),size=(400,400))
        layout = BoxLayout(orientation='vertical')
        pop.add_widget(layout)

        text_input = TextInput(multiline=False)
        layout.add_widget(text_input)

        button = Button(text="create",size_hint=(1,0.1))
        button.on_press = lambda: self.add_item(text_input.text)
        layout.add_widget(button)

        button_close = Button(text="close",size_hint=(1,0.1))
        button_close.on_press = pop.dismiss
        layout.add_widget(button_close)
        
        pop.open()

    def reset_itens(self):
        for item in self.itens.values():
            item.check._set_active(False)
            


    def to_json(self):
        data = super().to_json()
        data["type"] = "checklist"
        data["itens"] = []
        for item in self.itens.values():
            data["itens"].append((item.check.active,item.label.text))

        return data
        
    
    def from_json(self,data):
        super().from_json(data)
        self.layout.clear_widgets()
        for item in data["itens"]:
            self.add_item(item[1])
            self.itens[item[1]].check._set_active(item[0])

