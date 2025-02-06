from ..widgets.floatwidget import FloatWidget

from kivy.uix.textinput import TextInput

from kivy.uix.button import Button

from kivy.uix.rst import RstDocument

from kivy.uix.popup import Popup

from kivy.uix.boxlayout import BoxLayout

from m2r import convert



class Markdown(FloatWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Markdown")
        self.rst = RstDocument(pos_hint={'x': 0, 'y': 0})
        
        self.rst.colors = {"paragraph": "#33ff33","background": "#000000"}

        self.text = ""
        self.content.add_widget(self.rst)

        self.edit_button = Button(text="edit",pos_hint={'x': 4/6, 'y': -1/6},size_hint=(2/6,1/6))
        self.edit_button.on_press = self.on_edit
        self.content.add_widget(self.edit_button)


    def set_text(self,text):
        self.rst.text = convert(text)
        self.text = text

    def on_edit(self,*args):
        pop = Popup(title="Edit",size_hint=(None,None),size=(400,400))
        layout = BoxLayout(orientation='vertical')
        pop.add_widget(layout)

        text_input = TextInput(text=self.text)
        layout.add_widget(text_input)

        button = Button(text="ok",size_hint=(1,0.1))
        button.on_press = pop.dismiss
        layout.add_widget(button)

        pop.on_dismiss = lambda: self.set_text(text_input.text)
        pop.open()

    def to_json(self):
        data = super().to_json()
        data["type"] = "markdown"
        data["text"] = self.text

        return data
    
    def from_json(self,data):
        super().from_json(data)
        self.set_text(data["text"])




