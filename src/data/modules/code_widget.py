from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.codeinput import CodeInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from pygments.lexers.python import Python3Lexer


class Code(Popup):
    def __init__(self, **kwargs):
        super(Code, self).__init__(**kwargs)
        self.title = "Code"
        self.size_hint = (None, None)
        self.size = (400, 400)

        self.code = ""
        self.time_trigger = 1
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        self.code_input = CodeInput(text="", size_hint=(1, 0.9),style="emacs")
        layout.add_widget(self.code_input)

        self.time_label = Label(text="Time trigger:", size_hint=(1, 0.1))
        layout.add_widget(self.time_label)
        self.time_input = TextInput(text=str(self.time_trigger), size_hint=(1, 0.1))
        layout.add_widget(self.time_input)

        button = Button(text="OK", size_hint=(1, 0.1))
        button.on_press = self.on_ok
        layout.add_widget(button)

    def on_ok(self, *args):
        print("code:", self.code_input.text)
        self.code = self.code_input.text
        self.time_trigger = float(self.time_input.text)
        self.dismiss()

class ErrorPopup(Popup):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = BoxLayout(orientation="vertical")
        self.add_widget(self.box)
        self.label = Label(text=text)
        self.box.add_widget(self.label)
        self.title = "Error"
        self.size_hint = (0.4,0.4)
        self.button = Button(text="OK")
        self.button.on_press = self.dismiss
        self.box.add_widget(self.button)

        self.open()
