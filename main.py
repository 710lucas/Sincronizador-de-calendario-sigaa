from kivymd.app import MDApp as App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os

from login import *

class Login(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText
        self.ids["msg"].text = main(app.username, app.password)

        app.config.read(app.get_application_config())
        app.config.write()


    
    def open_browser():
        import webbrowser
        webbrowser.open('https://sigaa-sync.neocities.org/politica.html')

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))

        return manager

    def get_application_config(self):
        if(not self.username):
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

if __name__ == '__main__':
    LoginApp().run()