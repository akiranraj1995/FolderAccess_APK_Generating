import kivy

kivy.require('2.0.0')  # Replace with your Kivy version if needed

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import os


class FileExplorerApp(App):

    def build(self):
        # Set the initial directory path to the user's home directory
        self.current_path = os.path.expanduser("~")

        self.layout = BoxLayout(orientation="vertical")
        self.header = Label(text=self.current_path)
        self.file_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.file_list.bind(minimum_height=self.file_list.setter('height'))
        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

        self.back_button = Button(text="Back", size_hint=(None, None))
        self.back_button.bind(on_release=self.navigate_back)

        self.layout.add_widget(self.header)
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(self.scroll_view)
        self.scroll_view.add_widget(self.file_list)

        self.refresh_file_list(self.current_path)
        return self.layout

    def navigate_back(self, instance):
        if self.current_path != os.path.expanduser("~"):
            self.current_path = os.path.dirname(self.current_path)
            self.refresh_file_list(self.current_path)

    def refresh_file_list(self, path):
        self.header.text = path
        self.file_list.clear_widgets()

        files = os.listdir(path)
        for file in files:
            full_path = os.path.join(path, file)
            button = Button(text=file, size_hint_y=None, height=40)
            button.bind(on_release=self.on_file_selected(full_path))
            self.file_list.add_widget(button)

    def on_file_selected(self, full_path):
        def callback(instance):
            if os.path.isdir(full_path):
                self.current_path = full_path
                self.refresh_file_list(full_path)
            else:
                # Implement the file open action here
                pass

        return callback


if __name__ == '__main__':
    FileExplorerApp().run()
