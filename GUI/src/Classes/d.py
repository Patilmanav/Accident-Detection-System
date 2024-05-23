from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Welcome to Home Screen'))
        self.add_widget(Button(text='Go to Settings', on_press=self.go_to_settings))

    def go_to_settings(self, instance):
        self.manager.current = 'settings'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Welcome to Settings Screen'))
        self.add_widget(Button(text='Go back to Home', on_press=self.go_to_home))

    def go_to_home(self, instance):
        self.manager.current = 'home'

class TestApp(App):
    def on_stop(self):
        # return super().on_pause()
        print("App Paused")
        sm = self.root.current
        print(sm)
        return True
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == '__main__':
    TestApp().run()
