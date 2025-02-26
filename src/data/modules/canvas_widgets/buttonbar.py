from ..widgets.floatwidget import FloatWidget

from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout



class ButtonBar(FloatWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title("Button Bar")

        self.box_layout = BoxLayout(orientation='horizontal',size_hint=(1,1),pos_hint={'x':0,'y':0})
        self.content.add_widget(self.box_layout)
        self.scroll = ScrollView(size_hint=(1,1),pos_hint={'x':0,'y':0})
        self.box_layout.add_widget(self.scroll)

        self.stack = StackLayout(size_hint=(None,1),orientation='lr-tb',pos_hint={'x':0,'y':0},spacing = [10,25])
        self.stack.bind(minimum_width=self.stack.setter('width'))
        self.scroll.add_widget(self.stack)

        self.buttons = {}

        self.add_button = Button(text="+",size_hint=(1/8,1))
        self.add_button.background_color = self.theme["button-default"]
        self.add_button.background_normal = ""
        self.add_button.on_press = self.add_item_pop_up
        self.box_layout.add_widget(self.add_button)

        self.reset_button = Button(text="reset",size_hint=(1/8,1))
        self.reset_button.background_color = self.theme["button-default"]
        self.reset_button.background_normal = ""
        self.reset_button.on_press = self.reset_itens
        self.box_layout.add_widget(self.reset_button)

    def add_item_pop_up(self):
        popup = Popup(title="Adicionar Item", size_hint=(None, None), size=(400, 400))
        layout = BoxLayout(orientation='vertical')
        popup.content = layout

        text_input = TextInput()
        layout.add_widget(text_input)

        button = Button(text="OK", size_hint=(1, 0.1))
        button.on_press = lambda: self.add_item(text_input.text)
        layout.add_widget(button)
        

        popup.open()

    def add_item(self, text):
        button = Button(text=text,size_hint=(None,1),width=100)
        button.background_color = self.theme["button-default"]
        button.background_normal = ""
        self.stack.add_widget(button)
        self.buttons[text] = button
        self.stack.width += 125

        

    def reset_itens(self):
        self.stack.clear_widgets()
        del self.buttons
        self.buttons = {}

    def set_press_event(self, button, func):
        if self.buttons[button].on_press != func:
            self.buttons[button].on_press = func

    def to_json(self):
        data = super().to_json()
        data["type"] = "buttonbar"
        data["itens"] = []
        for item in self.buttons.values():
            data["itens"].append(item.text)

        return data
    

    def from_json(self,data):
        super().from_json(data)
        self.reset_itens()
        for item in data["itens"]:
            self.add_item(item)

    