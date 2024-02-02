import sqlite3

from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.graphics.svg import Window
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager
from kivy.animation import Animation, AnimationTransition
from kivy.properties import ListProperty
from kivy.uix.button import Button

from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

Window.size = (800, 600)

# <---- Database ---->

connector = sqlite3.connect('users.db')
curs = connector.cursor()
curs.execute("CREATE TABLE IF NOT EXISTS Login(Username VARCHAR, Password VARCHAR)")
connector.commit()

# <---- Widgets ---->

class HoverButtonMainPage(MDFillRoundFlatButton, ThemableBehavior, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor('hand')
        self.md_bg_color = (245/255, 195/255, 39/255, 0.8)
        self.text_color = (0, 0, 255, 0.5)
        self.line_color = (245/255, 131/255, 39/255, 0.8)
        Animation(size_hint=(.23, .13)).start(self)

    def on_leave(self):
        Window.set_system_cursor('arrow')
        self.md_bg_color = (0, 130/255, 242/255, 0.8)
        self.text_color = (1, 1, 1, 1)
        self.line_color = (0, 0, 0, 1)
        Animation(size_hint=(.2, .1)).start(self)


class HoverButtonPurpleDesign(MDFillRoundFlatButton, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor('hand')

    def on_leave(self):
        Window.set_system_cursor('arrow')

class HoverButton3(MDRaisedButton, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor('hand')

    def on_leave(self):
        Window.set_system_cursor('arrow')

class HoverButtonOriginal(Button, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor('hand')

    def on_leave(self):
        Window.set_system_cursor('arrow')

class HoverTextBox(MDTextField, HoverBehavior):
    def on_enter(self, *args):
        Window.set_system_cursor('hand')

    def on_leave(self, *args):
        Window.set_system_cursor('arrow')

# <---- Screens ---->

class MainPage(MDScreen):

    def animate_label_pop_up(self, *args):
        self.label = self.ids.title

        Animation(opacity=1, size_hint=(.2, .1), center = (Window.width/2, Window.height/2),
                  t='out_back', duration=1.5).start(self.label)
    def animate_label_movement(self, *args):
        self.label = self.ids.title

        anim = Animation(font_size=40, color=(0, 0, 198, 0.56), duration=1)
        anim += Animation(font_size=80, color=(0, 0, 0, 1), duration=1)
        anim.start(self.label)

        return self.label

class LoginPage(MDScreen):
    def on_enter(self):
        Window.set_system_cursor('arrow')
    def logIn(self):
        user_field = self.ids.uid
        pass_field = self.ids.pwd
        error_label = self.ids.error_label

        username = user_field.text
        password = pass_field.text

        curs.execute("SELECT * FROM Login WHERE Username = ? AND Password = ?", (username, password))
        data = curs.fetchone()

        if data is None:
            user_field.error = True
            pass_field.error = True
            error_label.text = "Incorrect username or password!"
            error_label.opacity = 1
            return
        else:
            error_label.opacity = 0

        self.manager.current = 'checks_page'

    def clear(self):
        self.ids.uid.text = ""
        self.ids.pwd.text = ""

# <---- App Class ---->

class SpectrumApp(MDApp):
    def build(self):
        self.icon = 'resources/puzzle.png'

        self.screen_manager = ScreenManager()

        self.main_screen = MainPage()
        self.label = self.main_screen.ids.title
        self.main_screen.animate_label_pop_up()

        Clock.schedule_interval(self.main_screen.animate_label_movement, 2)

        self.login_screen = LoginPage()

        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.login_screen)


        return self.screen_manager


SpectrumApp().run()