from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.graphics.svg import Window
from kivy.clock import Clock

from kivy.animation import Animation, AnimationTransition
from kivy.properties import ListProperty

from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.screen import MDScreen

Window.size = (800, 600)

# <---- Widgets ---->

class HoverButton(MDFillRoundFlatButton, ThemableBehavior, HoverBehavior):
    md_bg_color = ListProperty((0, 0, 255, 0.8))
    def on_enter(self):
        Window.set_system_cursor('hand')
        self.md_bg_color = (1, 1, 1, 1)
        self.text_color = (0, 0, 255, 0.5)
        self.line_color = (0, 0, 255, 0.8)
        Animation(size_hint=(.23, .13)).start(self)

    def on_leave(self):
        Window.set_system_cursor('arrow')
        self.md_bg_color= (0, 0, 255, 0.8)
        self.text_color = (1, 1, 1, 1)
        self.line_color = (0, 0, 0, 1)
        Animation(size_hint=(.2, .1)).start(self)

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

# <---- App Class ---->

class SpectrumApp(MDApp):
    def build(self):
        self.main_screen = MainPage()
        self.label = self.main_screen.ids.title
        self.main_screen.animate_label_pop_up()

        Clock.schedule_interval(self.main_screen.animate_label_movement, 2)

        return self.main_screen


SpectrumApp().run()