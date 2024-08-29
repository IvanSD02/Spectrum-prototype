# <---- Library imports ---->
import sqlite3
import re
import random
import datetime
import weakref
import geocoder
import pyttsx3
import webview

from webcolors import CSS3_HEX_TO_NAMES, hex_to_rgb
from scipy.spatial import KDTree

from kivymd.app import MDApp

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.graphics.svg import Window
from kivy import Config
from kivy.clock import Clock
from kivy.metrics import dp


from kivy.uix.screenmanager import ScreenManager
from kivy.animation import Animation, AnimationTransition
from kivy.properties import ListProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.behaviors import HoverBehavior, CommonElevationBehavior, FakeRectangularElevationBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem, IRightBodyTouch
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox

from kivy_garden.mapview import MapMarker


# <---- File imports ---->
import doodles.benzene_doodle as benzene_doodle
import doodles.stars_doodle as star_doodle
import doodles.colorful_tree_doodle as colorful_tree_doodle
import doodles.helix_doodle as helix_doodle
import doodles.tree_doodle as tree_doodle
import doodles.spiral_doodle as spiral_doodle

# <---- Configuration ---->
Window.size = (800, 600)
#fix
Config.set('graphics', 'resizable', False)

# <---- Constants ---->
#TODO - give meaningful names to the constants

ids_list = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13"]
list_of_all_functions = ["Daily Diary", "Emotions Diary", "Acknowledgements Diary", "To-Do List",
                         "Scheduler", "Text To Speech", "Shopping List", "Book Manager", "Hobby Roulette",
                         "Find Your Home!", "Speech To Text", "Chat Room", "Anti-Stress Doodles"]

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

boxes_ids_list = {"e10", "e2", "e6", "e4", "e9", "e7", "e1", "e13"}

theme_colors = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green',
                'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']


# <---- Utils ---->

def generate_map_of_functionalities(list_of_all_functions):
    map_of_all_functions_and_ids = {}
    for i in range(0, len(list_of_all_functions)):
        map_of_all_functions_and_ids[list_of_all_functions[i]] = 0

    return map_of_all_functions_and_ids

def convert_rgb_to_names(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []

    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'{names[index]}'

def create_datetime_format():
    # return current date in printable format
    today = datetime.date.today()
    week_day = datetime.date.weekday(today)

    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)

    return f"{days[week_day]}, {day}.{month}.{year}"

#TODO - fix function
def string_to_bool(value):
    if value.lower() in ('true', '1', 'yes'):
        return True
    elif value.lower() in ('false', '0', 'no'):
        return False
    else:
        return None

#tmp
functions_dict = generate_map_of_functionalities(list_of_all_functions)
print(functions_dict)

# <---- Database ---->

connector = sqlite3.connect('users.db')
curs = connector.cursor()

curs.execute("CREATE TABLE IF NOT EXISTS Login(Username VARCHAR, Password VARCHAR)")
connector.commit()

curs.execute("CREATE TABLE IF NOT EXISTS ToDo(P_Key INTEGER NOT NULL PRIMARY KEY, Title VARCHAR, Description VARCHAR, "
             "Priority VARCHAR, Date_Created VARCHAR, Due_Date VARCHAR, Active VARCHAR)")
connector.commit()

# <---- Widgets ---->
#TODO - Implement MDHeroTo
#TODO - fix all shadows (remove them, or see what 1.2 KV will offer)
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

class HoverButtonSaveChecks(MDRaisedButton, HoverBehavior):
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

class ElementCard(MDCard):
    pass

class TodoCard(CommonElevationBehavior, MDFloatLayout):

    title = StringProperty()
    description = StringProperty()
    image = StringProperty()
    date_created = StringProperty()
    due_date = StringProperty()
    out_done = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #fix
        if string_to_bool(self.done):
            self.ids.check.active = True
            self.ids.description.text = f"[s]{self.ids.description.text}[/s]"
            self.ids.bar.md_bg_color = 0, 179 / 255, 0, 1
    def effects(self, checkbox, value, id, title, description, bar):
        TODOListBox.on_complete(self, checkbox, value, id, title, description, bar)
    def remove_effects(self, button, id, title, description, bar):
        TODOListBox.on_remove(self, button, id, title, description, bar)
        self.ids.deleter.opacity = 0
        self.ids.deleter.disabled = True
        self.ids.check.opacity = 0
        self.ids.check.disabled = True

class VerticalDatePicker(MDDatePicker):
    pass

class HobbyCard(FakeRectangularElevationBehavior, MDFloatLayout):
    title = StringProperty()

class EmotionsCard(FakeRectangularElevationBehavior, MDFloatLayout):
    title = StringProperty()
    date = StringProperty()
    description = StringProperty()

class ContentEmotion(BoxLayout):
    pass

class ItemEmotion(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

class ItemCheckBox(IRightBodyTouch, MDCheckbox):
    pass


# <---- Screens ---->
#TODO - fix inconsistencies in design - use the same things, like change the screen only in KV, f.e
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

### Login, Signup and Account Management

class LoginPage(MDScreen):

    #TODO - make textboxes not red and empty when you exit screen
    #TODO - shadow does not disappear on reenter
    #TODO - hint background color blue
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

    #TODO - hint background color blue
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


class CheckFunctionalitiesPage(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def on_enter(self):
        Window.set_system_cursor('arrow')

        for id in ids_list:
            current_check_text = self.ids[id].text
            icons_id = self.ids[id + str(10)]
            for i in functions_dict:
                if current_check_text == i and functions_dict[i] == 1:
                    icons_id.active = True

    def check_click(self, instance, value, text):
        #TODO - No need for text variable - remove from KV file for all 13 checks
        #self.name = text

        for key in functions_dict:
            if text != key:
                continue
            functions_dict[key] = 1 if value else 0

        # for key in filter(lambda x: x != text, functions_dict.keys()):
        #     functions_dict[key] = 1 if value else 0

    def save_checked(self):
        self.manager.current = 'profile_page'

### Home Page Layout & Settings

class ProfilePage(MDScreen):

    # TODO - refactor heavily the emotions part
    def on_enter(self):
        Window.set_system_cursor('arrow')
        Window.size = (800, 600)

        for i in functions_dict:
            name_func = i
            if functions_dict[name_func] == 1:

                for j in boxes_ids_list:
                    if self.ids[j].text == name_func:
                        self.ids[j].disabled = False
            else:
                for j in boxes_ids_list:
                    if self.ids[j].text == name_func:
                        self.ids[j].disabled = True

    def enter_in_file_emoji(self, input_emoji):
        today = datetime.date.today()
        wd = datetime.date.weekday(today)

        #rework
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)

        file_in = open("resources/emotions.txt", 'a')

        #rework
        file_in.write(f"{days[wd]}, {day}.{month}.{year}")
        file_in.write("\n")
        file_in.write(input_emoji)
        file_in.write("\n")
        file_in.close()
        self.show_next_dialog()

    def enter_in_file_text(self, input_text):
        file_in = open("resources/emotions.txt", 'a')
        file_in.write(input_text)
        file_in.write("\n")
        file_in.write("\n")
        file_in.close()
        self.dialog_close(self)

    def create_page(self):
        #newCheck = CheckFunctionalitiesPage(name='checks_page_add')
        #self.manager.add_widget(newCheck)
        #self.manager.current = 'checks_page_add'
        self.manager.current = 'checks_page'

    def show_next_dialog(self):
        self.dialog = MDDialog(
            title="Why Is That?",
            type="custom",

            content_cls=ContentEmotion(),
            buttons=[
                MDFlatButton(
                    text="NOT NOW",
                    theme_text_color="Custom",
                    text_color="black",
                    on_release= lambda x: self.enter_in_file_text(self.dialog.content_cls.ids.field.text)
                ),
                MDFlatButton(
                    text="DONE!",
                    theme_text_color="Custom",
                    text_color="black",
                    on_release = lambda x: self.enter_in_file_text(self.dialog.content_cls.ids.field.text)#self.dialog.dismiss()
                ),
            ],
        )
        self.dialog.open()
    def dialog_close(self, obj):
        self.dialog.dismiss(force=True)

    def show_confirmation_dialog(self):
        self.dialog = MDDialog(
                title="How are you feeling today?",
                type="simple",
                items=[
                    ItemEmotion(text="Absolutely Joyful!", source="resources/happy.png", on_release=(lambda x: self.enter_in_file_emoji("Absolutely Joyful!")) ),
                    ItemEmotion(text="Really Happy!", source="resources/smile.png", on_release=(lambda x: self.enter_in_file_emoji("Really Happy!")) ),
                    ItemEmotion(text="Pretty Average.", source="resources/neutral.png", on_release=(lambda x: self.enter_in_file_emoji("Pretty Average.")) ),
                    ItemEmotion(text="A Bit Under The Weather...", source="resources/sad.png", on_release=(lambda x: self.enter_in_file_emoji("A Bit Under The Weather...")) ),
                    ItemEmotion(text="Tearful...", source="resources/cry.png", on_release=(lambda x: self.enter_in_file_emoji("Tearful...")) ),
                ])

        self.dialog.open()

    def drop_func(self, instance):
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "Will be organised",
                "on_release" : lambda x = "Example 1" : self.item1()
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Will be emotional freely",
                "on_release": lambda x="Example 2": self.item2()
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Will know your way home",
                "multiline": "True",
                "on_release": lambda x="Example 2": self.item3()
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Won't forget the groceries",
                "multiline":"True",
                "on_release": lambda x="Example 2": self.item4()
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Won't forget daily tasks",
                "multiline": "True",
                "on_release": lambda x="Example 2": self.item5()
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Won't spend hours decision-making.",
                "multiline": "True",
                "on_release": lambda x="Example 2": self.item6()
            },
            {
                "viewclass": "OneLineListItem",
                "text": "You will be yourself.",
                "multiline": "True",
                "on_release": lambda x="Example 2": self.item7()
            },
        ]

        self.menu = MDDropdownMenu(
            items = self.menu_list,
            width_mult = 5
        )

        self.menu.caller = instance
        self.menu.open()
    def change_theme(self, root):
        if root.theme_cls.theme_style == "Dark":
            root.theme_cls.theme_style = "Light"
        else:
            root.theme_cls.theme_style = "Dark"
    def show_theme_picker(self, root):
        random_color = random.choice(theme_colors)
        root.theme_cls.primary_palette = random_color
        root.theme_cls.accent_palette = random_color

    def change_but_color(self, app, root):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        rand = convert_rgb_to_names((r, g, b))

        self.ids.bot.icon_color = rand
        for i in boxes_ids_list:
            #print(root.ids[i].md_bg_color)
            root.ids[i].md_bg_color = rand

    def call_checks_page(self):
        self.manager.current = 'checks_page'
    pass

# <--- Application Screens --->

# To - Do List
class TODOListBox(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_entered_once = False
        self.date_created = create_datetime_format()
    def on_enter(self):
        Window.set_system_cursor('arrow')
        Window.size = (400, 600)

        # "0" -> active
        # "1" -> completed
        # "2" -> deleted

        #TODO - add a check to show completed tasks or not
        #TODO - fix problem with elevation on second entering in the to-do app
        #TODO - alert on a deadline
        #TODO - link to database for login to make todo individual

        #TODO - implement a sort by date
        #TODO - implement a priority rising by date
        #TODO - implement a deadline
        #TODO - implement random priority based on a deadline

        #TODO - fix design

        self.ids.date.text = self.date_created

        if self.has_entered_once:
            return

        curs.execute("SELECT * FROM ToDo")
        data = curs.fetchall()
        print(data)

        self.has_entered_once = True

        curs.execute("SELECT * FROM ToDo")
        data = curs.fetchall()

        done_tasks = []

        #better variant:
        #for line in data:
        #   out_id, out_title, out_desc, out_image, out_date_created, out_due_date, out_done = line


        for line in data:
            out_id = line[0]
            out_title = line[1]
            out_desc = line[2]
            out_image = line[3]
            out_date_created = line[4]
            out_due_date = line[5]
            out_done = line[6]

            if line == data[-1]:
                if out_done == "0":
                    self.add_todo_box(out_title, out_desc, out_image, out_due_date, 1, str(out_id),
                                      str(out_date_created))
                for task in done_tasks:
                    self.add_todo_box(*task)

            if out_done == "1":
                done_tasks.append([out_title, out_desc, out_image, out_due_date, 1, str(out_id),
                                      str(out_date_created), str(out_done)])
                continue

            if out_done == "2":
                continue

            self.add_todo_box(out_title, out_desc, out_image, out_due_date, 1, str(out_id), str(out_date_created))



    def on_complete(self, checkbox, value, ID, title, description, bar):

        original = description.text
        remove = ["[s]", "[/s]"]
        for i in remove:
            original = original.replace(i, "")

        if self.ids.check.active:
            description.text = f"[s]{description.text}[/s]"
            bar.md_bg_color = 0, 179/255, 0, 1
            Snackbar(text="Great job! One less thing to do!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(0, 179/255, 0, 1), font_size="18sp").open()
        else:
            description.text = original
            bar.md_bg_color = (1, 170/255, 23/255, 1)

        if self.ids.check.active:
            curs.execute("UPDATE ToDo SET Active= ? WHERE P_Key = ?", ("1", ID))
        else:
            curs.execute("UPDATE ToDo SET Active= ? WHERE P_Key = ?", ("0", ID))

        connector.commit()
        # test code
        curs.execute("SELECT * FROM ToDo")
        data = curs.fetchall()
        print(data)


    def on_remove(self, button, ID, title, description, bar):
        print("id" + ID)
        original = description.text
        remove = ["[s]", "[/s]"]
        for i in remove:
            original = original.replace(i, "")
        title.text += " (DELETED)"
        #title.text = f"[s]{title.text}[/s]"
        description.text = f"[s]{description.text}[/s]"
        bar.md_bg_color = "red"

        Snackbar(text="Task Removed", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                 size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                 bg_color=(255, 0, 0, 0), font_size="18sp").open()

        curs.execute("UPDATE ToDo SET Active= ? WHERE P_Key = ?", ("2", ID))
        connector.commit()

        # test code
        curs.execute("SELECT * FROM ToDo")
        data = curs.fetchall()
        print(data)



    def add_todo_box(self, title, description, image, due_date, on_enter, ID=None, date_created_task=None, out_done=None):
        # rework
        source_str = ''

        if image == '5':
            source_str = 'resources/priority/five.png'
        elif image == '4':
            source_str = 'resources/priority/four.png'
        elif image == '3':
            source_str = 'resources/priority/three.png'
        elif image == '2':
            source_str = 'resources/priority/two.png'
        else:
            source_str = 'resources/priority/one.png'

        curs.execute("SELECT * FROM ToDo")
        results = curs.fetchall()
        number_of_rows = len(results)

        date_created_task = self.date_created if not date_created_task else date_created_task
        week_day, data_format = date_created_task.split(" ")
        date_created_task = date_created_task.replace(week_day, "Created: ")

        new_due_date = " ".join(["Due: ", due_date])

        if title != "" and description != "" and image != "" and len(title) < 21 and len(description) < 61:
            self.manager.get_screen("todolist").todo_list.add_widget(TodoCard(id = str(number_of_rows + 1) if not ID else ID,
                            title = title, description = description, image = source_str , date_created = date_created_task,
                                                                            due_date = new_due_date, out_done = str(bool(out_done))))


            self.manager.get_screen("add_todo_box").title.text = ""
            self.manager.get_screen("add_todo_box").description.text = ""
            self.manager.get_screen("add_todo_box").priority.text = ""
            self.manager.get_screen("add_todo_box").due_date.text = "No Due"

            self.manager.current = 'todolist'

            if not on_enter:

                curs.execute("INSERT INTO ToDo (Title, Description, Priority, Date_Created, Due_Date, Active) VALUES (?, ?, ?, ?, ?, ?)",
                             (title, description, image, self.date_created, due_date, "0"))
                connector.commit()

                #test code
                curs.execute("SELECT * FROM ToDo")
                data = curs.fetchall()
                print(data)

        # get into function with text parameter
        elif title=="":
            Snackbar(text="Title is missing", snackbar_x="10dp", snackbar_y = "10dp", size_hint_y = .08, size_hint_x = (Window.width - (dp(10)*2))/Window.width,
                     bg_color=(1,170/255,23/255, 1), font_size = "18sp").open()

        elif description=="":
            Snackbar(text="Description is missing", snackbar_x="10dp", snackbar_y = "10dp", size_hint_y = .08, size_hint_x = (Window.width - (dp(10)*2))/Window.width,
                     bg_color=(1,170/255,23/255, 1), font_size = "18sp").open()

        elif image=="":
            Snackbar(text="Please, prioritise!", snackbar_x="10dp", snackbar_y = "10dp", size_hint_y = .08, size_hint_x = (Window.width - (dp(10)*2))/Window.width,
                     bg_color=(1,170/255,23/255, 1), font_size = "18sp").open()

        elif not len(title)<21:
            Snackbar(text="Title length is too long!(max: 20 characters)", snackbar_x="10dp", snackbar_y = "10dp", size_hint_y = .08, size_hint_x = (Window.width - (dp(10)*2))/Window.width,
                     bg_color=(1,170/255,23/255, 1), font_size = "18sp").open()

        elif not len(description)<61:
            Snackbar(text="Description length is too long!(max: 60 characters)", snackbar_x="10dp", snackbar_y = "10dp", size_hint_y = .08, size_hint_x = (Window.width - (dp(10)*2))/Window.width,
                     bg_color=(1,170/255,23/255, 1), font_size = "18sp").open()


class AddListBox(ThemableBehavior, MDScreen):
    #TODO - label should be once again "No Due" when one reenters
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_dialog = VerticalDatePicker()
        self.theme_cls.primary_palette = "Orange"

    def on_save(self, instance, value, date_range):
        formatted_date = value.strftime("%d.%m.%y")
        self.ids.due_date.text = str(formatted_date)
        self.theme_cls.device_orientation = "landscape"

    def on_cancel(self, instance, value):
        self.theme_cls.device_orientation = "landscape"
    def show_date_picker(self):
        self.date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        self.theme_cls.device_orientation = "portrait"
        self.date_dialog.open()


# Text To Speech

class TextToSpeech(MDScreen):
    # TODO - Adjust the volume of the speaker via a scroller
    # TODO - Save voice to a file - have a button next to speak (maybe the three buttons this, speak and clear are on one line?)
    # TODO - Have a button to clear the text
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
    def on_enter(self):
        Window.set_system_cursor('arrow')
        Window.size = (350, 490)
    def speak(self):
        self.engine.say(self.ids.text.text)
        self.engine.runAndWait()
    def change_voice_male(self):
        self.engine.setProperty('voice', self.voices[0].id) # 0 index is for male

    def change_voice_female(self):
        self.engine.setProperty('voice', self.voices[1].id) # 1 index is for male

    def on_leave(self):
        self.engine.stop()

# Hobby Roulette

class HobbyRoulette(MDScreen):
    # TODO - Implement PyQT Spinning Wheel
    # TODO - Center the label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_hobby = 0
    def on_enter(self, *args):
        Window.size = Window.size = (600, 600)

        file_out = open("resources/hobbies.txt", 'r')
        lines = file_out.readlines()
        if self.current_hobby != len(lines):
            for i in range(self.current_hobby, len(lines)):
                out_text = lines[i].strip()
                self.add_entry(out_text, True)

        current_hobby = len(lines)
        # file_out.close()

    def randomize(self):
        random_hobbies = []
        file_out = open("resources/hobbies.txt", 'r')
        lines = file_out.readlines()
        for i in lines:
            line = i.strip()
            random_hobbies.append(line)
        # print(randoms)
        random_hobby = random.choice(random_hobbies)
        self.ids.randomize.text = random_hobby
        file_out.close()

    def add_entry(self, title, is_in):
        self.manager.get_screen("hobbyroulette").hobbies_list.add_widget(HobbyCard(title=title))
        self.current_hobby += 1
        if not is_in:
            file_in = open("resources/hobbies.txt", 'a')
            file_in.write(title)
            file_in.write("\n")
            file_in.close()

# Anti-Stress Doodles

class AntistressDoodlesPage(MDScreen):
    # TODO - fix buttons formatting
    # TODO - do not exit after the turtle window is closed
    def on_enter(self):
        Window.set_system_cursor('arrow')

    def draw_benzene_screen(self):
        benzene_doodle.draw_benzene()

    def draw_tree_screen(self):
        tree_doodle.draw_tree()

    def draw_colorful_tree_screen(self):
        colorful_tree_doodle.draw_colorful_tree()

    def draw_spiral_screen(self):
        spiral_doodle.draw_spiral()

    def draw_helix_screen(self):
        helix_doodle.draw_helix()

    def draw_stars_screen(self):
        star_doodle.example_draw_stars()


# Emotions Diary

class Emotion(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_line = 0
    def on_enter(self):
        Window.size = (450, 600)
        file_out = open("resources/emotions.txt", 'r')
        lines = file_out.readlines()

        if self.current_line != len(lines):
            for i in range(self.current_line, len(lines), 4):
                out_date = lines[i]
                out_emoji = lines[i+1]
                out_text = lines[i+2]
                print(out_date)
                print(out_emoji)
                print(out_text)
                self.add_entry(out_date, out_emoji, out_text)

        current_line = len(lines)

    def add_entry(self, date, title, description):
        self.manager.get_screen("emotion").emotions_list.add_widget(EmotionsCard(date=date, title = title, description = description))

# Shopping List

class Shopping(MDScreen):
    #TODO - drag'n'drop with example png's
    #TODO - add list to the database of a user
    def on_enter(self):
        items = []
        for item in items:
            self.ids.list_item.add_widget(Factory.ListItem(text=item))
    def add_item(self):
        new_item = self.ids.new_item.text
        self.ids.list_item.add_widget(Factory.ListItem(text=new_item))
        self.ids.new_item.text = ""
    def remove_item(self):
        old_item = self.ids.new_item.text
    def change_screen(self):
        self.manager.current = 'profile_page'
    pass

# Find Your Home
class FindYourHome(MDScreen):
    #TODO - get coordinates from database
    #TODO - is it hardcoded? please, check - i think they are probably not used, remove them drom KV file (lat, lon, etc)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g = geocoder.ip('me')
        print(self.g.latlng)
        self.clicked = False

        self.latitude = 0.0
        self.longitude = 0.0

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude
    def on_enter(self, *args):
        self.ids.map.add_widget(MapMarker(lat=self.g.latlng[0], lon=self.g.latlng[1]))
        file_in = open("resources/homemap.txt", 'r')
        lines = file_in.readlines()
        self.latitude = lines[0].strip()
        self.longitude = lines[1].strip()

        marker = MapMarker(lat=self.latitude, lon=self.longitude, source="resources/housemarker.png")
        self.ids.map.add_widget(marker)
        self.ids['markermap'] = weakref.ref(marker)

        self.clicked = True
        file_in.close()

    def add_address(self, latitude, longitude):
        if not self.clicked:
            marker = MapMarker(lat=latitude, lon=longitude, source="resources/housemarker.png")
            self.ids.map.add_widget(marker)
            self.ids['markermap'] = weakref.ref(marker)
            self.clicked = True
            self.ids.latitude.text = self.latitude
            self.ids.longitude.text = self.longitude

        else:
            self.ids.map.remove_widget(self.ids.markermap)
            marker = MapMarker(lat=latitude, lon=longitude, source="resources/housemarker.png")
            self.ids.map.add_widget(marker)
            self.ids['markermap'] = weakref.ref(marker)

        file_out = open("resources/homemap.txt", 'w')
        file_out.write(latitude)
        file_out.write("\n")
        file_out.write(longitude)
        file_out.write("\n")
        file_out.close()


    def start_navigation(self):
        latitude = self.ids.latitude.text
        longitude = self.ids.longitude.text

        # Validate inputs
        if not latitude or not longitude:
            print("Please enter valid latitude and longitude.")
            return

        try:
            # Convert the inputs to float
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            print("Latitude and Longitude must be numbers.")
            return

        # Construct the Google Maps URL for navigation with maximum zoom
        google_maps_url = (
            f"https://www.google.com/maps/dir/?api=1&destination={latitude},{longitude}&travelmode=walking&dir_action=navigate&zoom=20"
        )

        # Open the URL in a new webview window
        webview.create_window('Google Maps Navigation', google_maps_url, width=800, height=600)
        webview.start()

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
        self.check_functionalities_page = CheckFunctionalitiesPage()
        self.profile_page = ProfilePage()

        self.todo_list_box = TODOListBox()
        self.add_todo_box = AddListBox()

        self.text_to_speech = TextToSpeech()
        self.hobby_roulette = HobbyRoulette()
        self.anti_stress_doodles = AntistressDoodlesPage()
        self.emotions_diary = Emotion()
        self.shopping_list = Shopping()
        self.find_your_home = FindYourHome()

        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.signup_screen)
        self.screen_manager.add_widget(self.successful_signup_screen)

        self.screen_manager.add_widget(self.choose_type_account_screen)
        self.screen_manager.add_widget(self.check_functionalities_page)
        self.screen_manager.add_widget(self.profile_page)

        self.screen_manager.add_widget(self.todo_list_box)
        self.screen_manager.add_widget(self.add_todo_box)

        self.screen_manager.add_widget(self.text_to_speech)
        self.screen_manager.add_widget(self.hobby_roulette)
        self.screen_manager.add_widget(self.anti_stress_doodles)
        self.screen_manager.add_widget(self.emotions_diary)
        self.screen_manager.add_widget(self.shopping_list)
        self.screen_manager.add_widget(self.find_your_home)


        return self.screen_manager


SpectrumApp().run()