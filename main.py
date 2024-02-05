import sqlite3
import re

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
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
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

class HoverTextBox(MDTextField, HoverBehavior):
    def on_enter(self, *args):
        Window.set_system_cursor('hand')

    def on_leave(self, *args):
        Window.set_system_cursor('arrow')

class HoverButtonOriginal(Button, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor('hand')

    def on_leave(self):
        Window.set_system_cursor('arrow')

class HoverButton3(MDRaisedButton, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor('hand')

    def on_leave(self):
        Window.set_system_cursor('arrow')

class CustomDialog(MDDialog):

    def open_strong_password_dialog(self):
        self.open()
    def dismiss_strong_password_dialog(self):
        self.dismiss(force=True)

class HoverCardChooseProfile(MDCard, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor('hand')
        self.md_bg_color = (245/255, 195/255, 39/255, 0.8)
        self.text_color = (0, 0, 255, 0.5)
        self.line_color = (245/255, 131/255, 39/255, 0.8)
        Animation(size_hint=(0.5, 0.7)).start(self)

    def on_leave(self):
        Window.set_system_cursor('arrow')
        self.md_bg_color = (255/255, 255/255, 255/255, 1)
        self.text_color = (1, 1, 1, 1)
        self.line_color = (0, 0, 0, 1)
        Animation(size_hint=(0.3, 0.5)).start(self)



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

    def change_screen(self):
        self.manager.current = "choose_type_account"

    def animate_loading_wheel(self):
        self.ids.circle.opacity = 1
        Clock.schedule_once(lambda _: self.change_screen(), 3)
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

        self.manager.transition.direction = "left"
        self.animate_loading_wheel()

    def clear(self):
        self.ids.uid.text = ""
        self.ids.pwd.text = ""

class SignupPage(MDScreen):
    def on_enter(self):
        Window.set_system_cursor('arrow')

    def strong_password_dialog(self):
        self.dialog = CustomDialog()
        return self.dialog

    def create_account(self):
        strong_password_regex = "^(?=(.*[a-z]){2,})(?=(.*[A-Z]){1,})(?=(.*[0-9]){1,})(?=(.*[!@#$%^&*()\-__+.]){1,}).{8,}$"

        user_field = self.ids.uid
        pass_field = self.ids.pwd
        repass_field = self.ids.repwd
        error_lab = self.ids.error_label

        username, password, repeat_password = user_field.text, pass_field.text, repass_field.text

        curs.execute("SELECT * FROM Login WHERE Username = ?", (username,))
        data = curs.fetchone()

        if data is not None:
            user_field.error = True
            error_lab.text = "Username already exists!"
            error_lab.opacity = 1
            return

        if not password or not username:
            user_field.error = True
            pass_field.error = True
            repass_field.error = True
            error_lab.text = "All fields have to be selected!"
            error_lab.opacity = 1
            return

        strong_password_pattern = re.compile(strong_password_regex)
        if not strong_password_pattern.match(password):
            pass_field.error = True
            repass_field.error = True

            if len(password) < 8:
                error_lab.text = "Please enter a valid password! (At least 8 symbols)"
            else:
                error_lab.text = "Please enter a valid password! (Must follow strong password guideline)"
                self.dialog = self.strong_password_dialog()
                self.dialog.open_strong_password_dialog()

            error_lab.opacity = 1
            return

        if len(password) <= 8:
            pass_field.error = True
            repass_field.error = True
            error_lab.text = "Please enter a valid password! (At least 8 symbols)"
            error_lab.opacity = 1
            return

        if password != repeat_password:
            pass_field.error = True
            repass_field.error = True
            error_lab.text = "Passwords must match!"
            error_lab.opacity = 1

        else:
            self.manager.current = 'success'
            pass_field.error = False
            repass_field.error = False
            error_lab.opacity = 0

            curs.execute("INSERT INTO login (Username, Password) VALUES (?, ?)", (username, password))
            connector.commit()

class SuccessfulSignupPage(MDScreen):
    def on_enter(self):
        Window.set_system_cursor('arrow')
    pass

class ChooseTypeAccountPage(MDScreen):
    def on_enter(self):
        Window.set_system_cursor('arrow')



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
        self.signup_screen = SignupPage()
        self.successful_signup_screen = SuccessfulSignupPage()

        self.choose_type_account_screen = ChooseTypeAccountPage()

        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.signup_screen)
        self.screen_manager.add_widget(self.successful_signup_screen)

        self.screen_manager.add_widget(self.choose_type_account_screen)


        return self.screen_manager


SpectrumApp().run()