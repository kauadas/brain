from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView


class FileExplorer(Popup):
    def __init__(self,is_save=False, file_chooser_options={},**kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        self.file_chooser = FileChooserIconView(size_hint=(1, 0.9),**file_chooser_options)
        layout.add_widget(self.file_chooser)

        self.infra = StackLayout(orientation='lr-tb',size_hint=(1,0.1))
        layout.add_widget(self.infra)

        self.is_save = is_save

        button_ok = Button(text="OK",size_hint=(0.30,1))

        if self.is_save:
            self.save_file = None
            self.file_name = TextInput(hint_text="File name",size_hint=(0.4,1),multiline=False)
            self.infra.add_widget(self.file_name)
            button_ok.on_press = self.save

        else:
            self.load_file = None
            button_ok.on_press = self.load

        self.infra.add_widget(button_ok)

        button_cancel = Button(text="Cancel",size_hint=(0.30,1))
        button_cancel.on_press = self.dismiss
        self.infra.add_widget(button_cancel)

    def load(self,*args):
        self.load_file = self.file_chooser.selection[0]
        print(self.load_file)
        self.on_ok()
        self.dismiss()

    def save(self,*args):
        if self.file_chooser.selection:
            self.save_file = self.file_chooser.selection[0]
        
        else:
            path = self.file_chooser.path
            file_name = self.file_name.text
            self.save_file = path+"/"+file_name

        print(self.save_file)
        self.on_ok()
        self.dismiss()

    def on_ok(self,*args):
        pass


        

    
if __name__ == "__main__":
    from kivy.app import runTouchApp

    file_chooser_options = {
        'path': '/home/kua'
    }
    runTouchApp(FileExplorer(is_save=True,file_chooser_options=file_chooser_options))