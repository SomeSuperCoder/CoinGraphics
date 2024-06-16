import time

from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from search import search
from kivymd.uix.list import IconLeftWidget
import pandas
import os

import random
from kivy.clock import mainthread
import json
import threading
import kvant_lib
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from kivy.properties import ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineIconListItem, TwoLineIconListItem
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
import hashlib
import random
import requests
from url import url

from pathlib import Path

home_dir = str(Path.home())

device = "windows"

if 'ANDROID_ARGUMENT' not in os.environ and 'ANDROID_PRIVATE' not in os.environ:
    Window.size = (520, 900)
else:
    device = "android"


def get_account(login):
    result = json.loads(requests.get(f"{url}/get_account/{login}").text)
    return result


def md5sum(value):
    return hashlib.md5(value.encode()).hexdigest()


class Content(BoxLayout):
    pass


class Item(OneLineAvatarIconListItem):
    left_icon = StringProperty()
    right_icon = StringProperty()
    right_text = StringProperty()


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MenuHeader(MDBoxLayout):
    '''An instance of the class that will be added to the menu header.'''


class SigInt:
    def __init__(self):
        self.val = False

    def set(self, val):
        self.val = val


class MoneyTest(MDApp):
    dialog_report_open = None
    level = ""
    dialog_list = None
    dialog_change = None
    dialog_lan = None
    dialog_accrual = None
    dialog_confirmation = None
    dialog_settings_account = None
    dialog_confirmation_report = None
    dialog_for_send = None
    name = str
    password = str
    id = str
    dialog_loading = None
    birthday = str
    user_modified = str
    icon = "scr/logo (2).png"
    title = "Kvantomat"
    charge_contests = None
    text_search = ""
    path = ""
    balance = 0
    thread_end = True
    search_handle: threading.Thread = None
    search_sig_int = SigInt()
    id_object_remove = ""
    children = None
    filename = None
    sig_stop_all = False
    id_teacher = ""
    # try:
    #     children = json.loads(requests.get(f"{url}/get_account_skeleton_list").text)
    # except json.decoder.JSONDecodeError:
    #     print("The Server is not responding")

    # def update_list(self):
    #     while True:
    #         if self.sig_stop_all:
    #             break
    #         time.sleep(3.5)
    #         try:
    #             self.children = json.loads(requests.get(f"{url}/get_account_skeleton_list").text)
    #         except json.decoder.JSONDecodeError:
    #             print("The Server is not responding")

    # def on_start(self):
    #     self.handle = threading.Thread(target=self.update_list).start()

    def on_stop(self):
        self.sig_stop_all = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Window.bind(on_keyboard=self.events)
        self.fg = None
        self.elevation = 0

    def manager_file_exel_open(self):
        import crossfiledialog
        self.filename = crossfiledialog.open_file(start_dir=home_dir, filter="*.xlsx")
        if not self.filename:
            toast("Вы не выбрали файл")
            return
        self.clear_list(self.root.ids.list_students_other_teachers)
        threading.Thread(target=self.excel_read).start()

    def generate(self):
        while True:
            value = random.randint(10_000, 99_999)
            if not get_account(value):
                return value

    @mainthread
    def loading_windows(self, i, data):
        if not self.dialog_loading:
            self.dialog_loading = MDDialog(
                title="Загрузка...",
                text=f'{i}/',
                auto_dismiss=False
            )
        self.dialog_loading.open()
        self.dialog_loading.text = f"{i + 1}/{len(data)} Человек"
        if i + 1 == len(data):
            self.dialog_loading.dismiss()

    def excel_read(self):
        try:
            print(self.filename)
            df = pandas.read_excel(f'{self.filename}')
            birthday = df['Дата рождения']
            name = df['ФИО']
            generates = self.generate()
            data = []
            for i in range(len(birthday)):
                birthday_enter = birthday[i]
                password = "12345678"
                check = json.loads(requests.get(f"{url}/does_exist_pair?name={name[i]}&birthdate={birthday_enter}").text)
                print(f"Check: {check}")
                if check is not None:
                    account = get_account(check)
                    generates = check
                    password = "Уже есть"
                else:
                    generates = self.generate()
                self.loading_windows(i, birthday)
                data.append(
                        [f"{generates}", f"{name[i]}", f'{birthday_enter}', f"{password}"])
            birthday_list = []
            id_list = []
            name_list = []
            enter_list = []
            password_list = []
            print("PRINT1!")
            for i in range(len(data)):
                id_list.append(data[i][0])
                name_list.append(data[i][1])
                birthday_list.append(data[i][2])
                password_list.append(data[i][3])
            print("PRINT1@")
            enter_list.append(["ID", id_list])
            enter_list.append(["ФИО", name_list])
            enter_list.append(["Дата рождение", birthday_list])
            enter_list.append(["Пароль", password_list])
            enter_list = dict(enter_list)
            df = pandas.DataFrame(enter_list)
            df.to_excel('./list_user.xlsx')
            self.table_create(data)
            print(f"Data: {data}")
        except KeyError:
            self.send_message("Неправильные столбцы")

    @mainthread
    def send_message(self, message):
        toast(message)

    @mainthread
    def table_create(self, data):
        self.charge_contests = MDDataTable(
            size_hint=(0.9, 1),
            rows_num=len(data),
            column_data=[
                ("ID", dp(10)),
                ("ФИО", dp(52)),
                ("Дата рождения", dp(19)),
                ("Пароль", dp(19.2)),
            ],
            row_data=[
                [
                    f"{data[i][0]}",
                    f"{data[i][1]}",
                    f"{data[i][2]}",
                    f"{data[i][3]}"
                ] for i in range(len(data))
            ],
        )
        self.root.ids.generate_table.add_widget(self.charge_contests)
        toast(f"{self.path}")
        self.root.ids.boxlayout_download.pos_hint = ({"center_x": .3, "center_y": .1})
        self.root.ids.action_send_message.text = "create"

    def create_users_sql(self):
        self.dialog_email_send("list_user.xlsx")

        for i in range(len(self.charge_contests.row_data)):
            if self.charge_contests.row_data[i][3] == "Уже есть":
                self.send_message("Aккаунт создан")
            else:
                json = kvant_lib.create_user(self.charge_contests.row_data[i][0], self.charge_contests.row_data[i][1], self.charge_contests.row_data[i][2], "12345678", self.root.ids.login.text, self.root.ids.password.text)
                requests.post(url=f"{url}/execute", data=json.encode("utf-8"))

    def notification(self):
        self.root.ids.notification_bell.icon = 'bell-ring'

    def send_mail(self, file_name: str):
        if len(self.dialog_for_send.content_cls.ids.email_for_send.text) == 0:
            toast("Введите почту")
        else:
            with open(file_name, "rb") as f:
                a = f.read()
                json = kvant_lib.send_mail(self.dialog_for_send.content_cls.ids.email_for_send.text, a, "Список учеников", self.root.ids.login.text, self.root.ids.password.text)
                requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
            self.screen("teacher_screen")
            self.dialog_close("dialog_for_send")

    def threading_search(self, text):
        if self.search_sig_int.val:
            self.search_sig_int.set(True)
            self.search_handle.join()
            self.search_sig_int.set(False)
            self.clear_list(self.root.ids.container)

        self.search_handle = threading.Thread(target=self.search_students,args=(text,))
        self.search_handle.start()

    def search_students(self, text=""):
        my_list = []
        # if len(text) < len(self.text_search):
        #     self.text_search = text
        #     return

        if len(text) > 2:
            self.clear_list(self.root.ids.container)
            search_person = json.loads(requests.get(f"{url}/get_account_skeleton_list").text)
            LIST = search(search_person, text, self.search_sig_int)
            if LIST is None:
                return
            for i in LIST:
                if self.search_sig_int.val:
                    return
                my_list.append(search_person[i])

            self.clear_list(self.root.ids.container)
            for i in my_list:
                self.string_person(i)
            self.text_search = text

    @mainthread
    def clear_list(self, id):
        id.clear_widgets()

    @mainthread
    def string_person(self, puple):
        self.root.ids.container.add_widget(
            ThreeLineIconListItem(
                text=puple['name'],
                secondary_text=puple['birthdate'],
                tertiary_text=f"ID: {puple['id']}",
                on_release=lambda x: self.dialog_windows(x, "teacher_screen")
            ),
        )

    def balance_def(self, ids):
        id_user = ids.replace("ID: ", "")
        balance = json.loads(requests.get(f"{url}/get_account/{id_user}").text)["balance"]
        if self.dialog_list:
            self.dialog_list.text = f'Баланс: {balance}'
        return balance

    def dialog_windows(self, task_windows, screen):
        print(task_windows.text, task_windows.secondary_text)
        self.name = task_windows.text
        self.birthday = task_windows.secondary_text
        self.id = task_windows.tertiary_text
        print(screen)
        self.root.ids.button_back_group.on_release = lambda: self.screen(screen)
        if self.dialog_list:
            self.dialog_list = None
        if not self.dialog_list:
            self.dialog_list = MDDialog(
                title=f"{self.name}",
                text=f"Баланс: Загрузка...",
                type="simple",
                radius=[20, 7, 20, 7],
                items=[
                    Item(text="Удалить", on_release=lambda x=task_windows.text: self.send_message("У вас нет доступа") if screen == "screen_students_teachers" else self.dialog_windows_task(x)),
                    Item(text="Сбросить пароль", on_release=lambda x=task_windows.text: self.send_message("У вас нет доступа") if screen == "screen_students_teachers" else (lambda x=task_windows.text: self.dialog_windows_task(x))),
                    Item(text="Начислить", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                    Item(text="Списание", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                    Item(text="История", on_release=lambda x: threading.Thread(target=self.history_threading, args=(task_windows.tertiary_text, self.root.ids.list_history_students_admin,)).start())
                ],

            )
            self.dialog_list.open()
            threading.Thread(target=self.balance_def, args=(self.id,)).start()

    def history_threading(self, login, list_id):
        print(login)
        balance = 0
        if type(login) == str:
            self.root.ids.spinner_history_accruals.active = True
            self.dialog_close("dialog_list")
            self.screen("history_students")
            login = login.replace("ID: ", "")
            account = get_account(login)
            history = account["history"]
        else:
            self.root.ids.spinner_history_accruals.active = True
            login = login.text.replace("ID: ", "")
            print(login)
            account = get_account(login)
            history = account["history"]
            balance = account['balance']
        self.history_not_threading(history, list_id, balance)

    @mainthread
    def history_not_threading(self, history, list_id, balance):
        list_id.clear_widgets()
        for i in reversed(history):
            list_id.add_widget(
                ThreeLineIconListItem(
                    IconLeftWidget(
                        icon="history"
                    ),
                    text=str(i['sum']),
                    secondary_text=f"{i['for_what']}",
                    tertiary_text=str(i['time'])
                ))
        self.root.ids.balance_user.text = f"{balance} Kvant"
        self.root.ids.spinner_history_accruals.active = False
        self.root.ids.spinner_history_student.active = False

    @mainthread
    def dialog_close(self, a):
        eval(f"self.{a}.dismiss()")

    @mainthread
    def dialog_email_send(self, file_name: str):
        if not self.dialog_for_send:
            self.dialog_for_send = MDDialog(
                radius=[20, 7, 20, 7],
                title="Введите почту",
                type="custom",
                auto_dismiss=True if file_name == "template.xlsx" else False,
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="email_for_send",
                        hint_text="Почта",
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="60dp",
                ),
                buttons=[
                    MDFlatButton(
                        text="Отправить",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.send_mail(file_name)
                    ),
                ],

            )
        self.dialog_for_send.open()

    def dialog_windows_change(self):
        self.dialog_close("dialog_list")
        if self.dialog_change:
            self.dialog_change = None
        if not self.dialog_change:
            self.dialog_change = MDDialog(
                radius=[20, 7, 20, 7],
                title=f"",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="first_field",
                        input_filter='float',
                        hint_text=f"Пароль",
                    ),
                    MDTextField(
                        id="secondary_field",
                        hint_text=f"Потвердите пароль",
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="120dp",
                ),
                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog_close("dialog_change")
                    ),
                    MDFlatButton(
                        text="Отредактировать",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.threading_examination_setting()
                    ),
                ],

            )
            self.dialog_change.open()

    def dialog_windows_confirmation(self):
        if not self.dialog_confirmation:
            self.dialog_confirmation = MDDialog(
                title=f"Вы точно хотите удалить: \n{self.name}",
                text="Все данные о пользователе будут стерты безвозратно",
                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog_close("dialog_confirmation")
                    ),
                    MDFlatButton(
                        text="Да",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.threading("clear_account")
                    ),
                ],
            )
        self.dialog_confirmation.open()

    def clear_account(self):
        id = self.id.replace("ID: ", "")
        self.dialog_close("dialog_confirmation")
        self.dialog_close("dialog_list")
        if self.dialog_confirmation.text == "Все данные о пользователе будут стерты безвозратно":
            json = kvant_lib.delete_user(id, self.root.ids.login.text, self.root.ids.password.text)
            requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
            print(self.id_object_remove)
            print(self.root.ids.my_list_students)
            self.send_message("Аккаунт удален")
        else:
            json = kvant_lib.change_password(id, "12345678",self.root.ids.login.text, self.root.ids.password.text)
            requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
            self.send_message("Пароль сброшен")
        self.threading_action("self.root.ids.container.clear_widgets()")
        self.threading_action("self.root.ids.list_students_other_teachers.clear_widgets()")
        self.threading_action("self.root.ids.my_list_students.clear_widgets()")

    @mainthread
    def threading_action(self, action):
        eval(action)

    def dialog_windows_task(self, task):
        task = task.text
        if task == "Сбросить пароль":
            self.dialog_windows_confirmation()
            self.dialog_confirmation.text = "Пароль будет по умолчанию: 12345678"
            self.dialog_confirmation.title = f"Вы точно хотите сбросить пароль: \n{self.name}?"
        elif task == "Удалить":
            self.dialog_windows_confirmation()
            self.dialog_confirmation.text = f"Все данные о пользователе будут стерты безвозратно"
            self.dialog_confirmation.title = f"Вы точно хотите удалить: \n{self.name}?"
        elif task == "Начислить":
            self.dialog_windows_change()
            self.dialog_change.title = "Начислить"
            self.dialog_change.content_cls.ids.first_field.hint_text = "Сколько"
            self.dialog_change.content_cls.ids.secondary_field.hint_text = "За что"
        elif task == "Списание":
            self.dialog_windows_change()
            self.dialog_change.title = "Списать"
            self.dialog_change.content_cls.ids.first_field.hint_text = "Сколько"
            self.dialog_change.content_cls.ids.secondary_field.hint_text = "За что"

    def menu_callback(self, text_item):
        self.level = f"{text_item}"
        self.root.ids.drop_menu_position.text = f"{text_item}"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_file("kivy.kv")

    def threading_examination_setting(self):
        if not self.thread_end:
            print(self.thread_end)
            return
        self.thread_end = False
        self.threading("settings_balance")

    def settings_balance(self):
        try:
            sum = int(self.dialog_change.content_cls.ids.first_field.text)
            if str(sum)[0] == '-':
                self.send_message("Введите положительное число")
                self.thread_end = True
                return
            balance = int(self.dialog_list.text.replace("Баланс: ", ""))
            print(type(balance))
            print(self.id)
            id = self.id.replace("ID: ", "")
            print(self.dialog_change.title)
            if self.dialog_change.title == "Списать":
                if balance < sum:
                    self.send_message("Недостаточно средст")
                else:
                    json = kvant_lib.change_balance(-sum, id, self.dialog_change.content_cls.ids.secondary_field.text, self.root.ids.login.text, self.root.ids.password.text)
                    self.send_message("Списано")
                    self.dialog_close("dialog_change")

            elif self.dialog_change.title == "Начислить":
                json = kvant_lib.change_balance(sum, id, self.dialog_change.content_cls.ids.secondary_field.text, self.root.ids.login.text, self.root.ids.password.text)
                self.send_message("Начислино")
                self.dialog_close("dialog_change")
            requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
        except ValueError:
            self.send_message("Введите сумму начисления")
        self.thread_end = True
        print("564", self.thread_end)

    def threading(self, fun):
        eval(f"threading.Thread(target=self.{fun}).start()")

    def dialog_report(self):
        if not self.dialog_report_open:
            self.dialog_report_open = MDDialog(
                radius=[20, 7, 20, 7],
                title="Куда отправить",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="email_field",
                        hint_text="Почта",
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="60dp",
                ),
                buttons=[
                    MDFlatButton(
                        text="Отправить",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.send_report()
                    ),
                ],

            )
        self.dialog_report_open.open()

    def send_report(self):
        try:
            if len(self.dialog_report_open.content_cls.ids.email_field.text) == 0:
                return toast("Введите почту")
            threading.Thread(target=self.threading_report).start()
            toast("Отчет придет в течение минуты")
            self.dialog_close("dialog_report_open")
        except json.decoder.JSONDecodeError:
            self.send_message("Ошибка сервера")

    def update(self):
        threading.Thread(target=self.history_threading, args=(self.root.ids.login, self.root.ids.scroll_history,)).start()

    def registration(self):
            login = self.root.ids.login_admin_new.text
            password = self.root.ids.password_admin_new.text
            name = self.root.ids.name_admin_new.text
            birthday = self.root.ids.birthday_admin_new.text
            email = self.root.ids.email_new_admin.text

            for i in (login, password, name, birthday, email):
                if not len(i):
                    toast("Вы заполнили не все поля")
                    return
            
            if get_account(login):
                toast("Такой логин есть")
            else:
                print("My login is:")
                print(self.root.ids.login.text)
                json = kvant_lib.create_user(login, name, birthday, password, self.root.ids.login.text, self.root.ids.password.text)
                requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
                self.screen("admin_screen")
                toast("Создали аккаунт")

    def dialog_settings_accounts(self):
        if not self.dialog_settings_account:
            self.dialog_settings_account = MDDialog(
                title="Измените пароль по умолчанию",
                type="custom",
                auto_dismiss=False,
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="password_input",
                        hint_text=f"Пароль",
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="60dp",
                ),
                buttons=[
                    MDRaisedButton(
                        text="Изменить",
                        on_release=lambda x: self.settings_password()
                    ),
                ],
            )
        self.dialog_settings_account.open()

    def user_scroll_balance(self, ids):
        pass

    def settings_password(self):
        requests.get(f"{url}/passwd?login={self.root.ids.login.text}&new_password={hashlib.sha256(self.dialog_settings_account.content_cls.ids.password_input.text.encode()).hexdigest()}")
        self.dialog_close("dialog_settings_account")

    def log_in(self):
        try:
            login = self.root.ids.login.text
            password = self.root.ids.password.text
            self.root.ids.spinner_login_screen.active = True
            print("Pre check")
            check = requests.get(f"{url}/check_login_credentials?login={login}&password={hashlib.sha256(password.encode()).hexdigest()}").text
            print(f"The check is: {check}")
            check = json.loads(check)
            if check:
                account = get_account(login)
                if len(login) == 5:
                    time.sleep(2)
                self.login_interface(login, password, account)
            else:
                self.send_message("Введены неверные данные")
                self.root.ids.spinner_login_screen.active = False
        except json.decoder.JSONDecodeError:
            self.send_message("Тех. перерыв")
            self.root.ids.spinner_login_screen.active = False

    @mainthread
    def login_interface(self, login, password, account):
        print("We are in login_interface")
        id_ = account["id"]
        fullname = account["name"]
        balance = account["balance"]
        history = account["history"]
        birthdate = account["birthdate"]

        name = dict(enumerate(fullname.split(" "))).get(1) or fullname
        family = dict(enumerate(fullname.split(" "))).get(0) or fullname
        dad = dict(enumerate(fullname.split(" "))).get(2) or fullname
        toast("Вы вошли")
        if len(login) == 5:
            self.id = login
            self.password = password
            self.root.ids.screen_manager.current = "main_screen"
            print(history)
            self.history_not_threading(history, self.root.ids.scroll_history, balance)
            self.root.ids.balance_user.text = f"{balance} Kvant"
            self.root.ids.name_profile_main.text = f"{family} {name} \n{dad}"
            self.root.ids.name_main_screen.text = f"{name} >"
            charge_contests = MDDataTable(
                column_data=[
                    ("Уровни", dp(38)),
                    ("1 место", dp(14)),
                    ("2 место", dp(14)),
                    ("3 место", dp(14)),
                    ("Участие", dp(14)),
                ],
                row_data=[
                    (
                        "Кванториум_НЧК",
                        "3",
                        "2",
                        "1",
                        "-",
                    ),
                    (
                        "Городской",
                        "5",
                        "3",
                        "2",
                        "1",
                    ),
                    (
                        "Республиканский",
                        "7",
                        "5",
                        "3",
                        "2"
                    ),
                    (
                        "Межрегиональный",
                        "10",
                        "7",
                        "5",
                        "3",
                    ),
                    (
                        "Всероссийский",
                        "15",
                        "10",
                        "7",
                        "5",
                    ),
                ],
            )
            self.root.ids.charge_contests.add_widget(charge_contests)
        elif len(login) == 6:
            self.root.ids.screen_manager.current = "teacher_screen"
            self.root.ids.name_teacher_screen.text = name
            self.root.ids.id_teacher_screen.text = id_
            self.root.ids.platform_device.text = device
            self.root.ids.birthday_teacher_screen.text = birthdate
        elif len(login) == 7:
            self.root.ids.platform_device.text = device
            self.root.ids.screen_manager.current = "teacher_screen"
            self.root.ids.admin_name.text = account["name"]
            self.root.ids.name_teacher_screen.text = "Администрация"
            self.root.ids.birthday_teacher_screen.text = "26.11.1991"
            self.root.ids.id_teacher_screen.text = 'admin'
        if password == "12345678":
            self.dialog_settings_accounts()
        self.root.ids.spinner_login_screen.active = False

    @mainthread
    def screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name
        self.screen_open = screen_name

    def threading_report(self):
        a = json.loads(requests.get(f"{url}/get_raiting_skeleton").text)
        sorted_dict = dict(sorted(a.items(), key=lambda item: item[1], reverse=True))
        name_list = []
        rating_list = []
        enter_list = []
        for i in sorted_dict.keys():
            name_list.append(i)
            rating_list.append(sorted_dict[i])
        enter_list.append(["ФИО", name_list])
        enter_list.append(["Рейтинг", rating_list])
        enter_list = dict(enter_list)
        df = pandas.DataFrame(enter_list)
        df.to_excel('./rating_list.xlsx')

        with open("./rating_list.xlsx", "rb") as f:
            a = f.read()
            send = kvant_lib.send_mail(self.dialog_report_open.content_cls.ids.email_field.text, a, "Отчёт о рейтинге",
                                       self.root.ids.login.text, self.root.ids.password.text)
            print(self.dialog_report_open.content_cls.ids.email_field.text)
            requests.post(url=f"{url}/execute", data=send.encode("utf-8"))

    def confirmation_report(self):
        if not self.dialog_confirmation_report:
            self.dialog_confirmation_report = MDDialog(
                title=f"Вы точно хотите cбросить полугодие?",
                text="Полугодие будет закрыто и отчет начнется заново",
                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog_close("dialog_confirmation_report")
                    ),
                    MDFlatButton(
                        text="Да",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.threading("reset_rating")
                    ),
                ],
            )
        self.dialog_confirmation_report.open()

    def reset_rating(self):
        json = kvant_lib.reset_raiting(self.root.ids.login.text, self.root.ids.password.text)
        requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
        self.dialog_close("dialog_confirmation_report")
        print("Конец")

    def group_teachers(self):
        self.root.ids.spinner_my_students.active = True
        self.root.ids.spinner_teachers.active = True
        self.screen("groups_list")
        children = json.loads(requests.get(f"{url}/get_account_skeleton_list").text)
        self.clear_list(self.root.ids.my_list_students)
        self.clear_list(self.root.ids.list_teachers)
        self.row_students(self.root.ids.login.text, self.root.ids.my_list_students, children, "groups_list")
        self.list_teachers(children)


    @mainthread
    def list_teachers(self, children):
        for key, item in children.items():
            if len(key) == 6:
                self.root.ids.list_teachers.add_widget(
                    TwoLineIconListItem(
                        text=item.get("name"),
                        secondary_text=f"ID: {item.get('id')}",
                        on_release=lambda x: threading.Thread(target=self.showing_other_students, args=(x,)).start()
                    ),
                )
        self.root.ids.spinner_teachers.active = False

    def showing_other_students(self, x):
        children = json.loads(requests.get(f"{url}/get_account_skeleton_list").text)
        id_name = x.secondary_text.replace("ID: ", "")
        self.id_teacher = id_name
        self.screen("screen_students_teachers")
        self.clear_list(self.root.ids.list_students_other_teachers)
        self.root.ids.spinner_students_teacher.active = True
        print("adadadad")
        self.row_students(id_name, self.root.ids.list_students_other_teachers, children, "screen_students_teachers")
        self.root.ids.spinner_students_teacher.active = False

    @mainthread
    def row_students(self, id_name, id_list, children, screen):
        for key, item in children.items():
            if item.get("creator") == id_name:
                id_list.add_widget(
                    ThreeLineIconListItem(
                        text=item.get("name"),
                        secondary_text=str(item.get("balance")),
                        tertiary_text=f"ID: {item.get('id')}",
                        on_release=lambda x: self.dialog_windows(x, screen)
                    ),
                )
        self.root.ids.spinner_my_students.active = False

    def give_to_all_dialog(self, of):
        if self.dialog_accrual:
            self.dialog_accrual = None
        if not self.dialog_accrual:
            self.dialog_accrual = MDDialog(
                radius=[20, 7, 20, 7],
                title=f"",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="sum_field",
                        input_filter='float',
                        hint_text=f"Сумма",
                    ),
                    MDTextField(
                        id="what_field",
                        hint_text=f"За что",
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="120dp",
                ),
                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog_close("dialog_change")
                    ),
                    MDFlatButton(
                        text="Начислить",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: threading.Thread(target=self.give_to_all, args=(of,)).start()
                    ),
                ],

            )
            self.dialog_accrual.open()

    def give_to_all(self, of):
        self.dialog_close("dialog_accrual")
        children = json.loads(requests.get(f"{url}/get_account_skeleton_list").text)
        for key, item in children.items():
            id_name = self.root.ids.login.text if of=='mine' else self.id_teacher
            amount = int(self.dialog_accrual.content_cls.ids.sum_field.text)
            for_what = self.dialog_accrual.content_cls.ids.what_field.text
            print(amount, key, for_what)
            if item.get("creator") == id_name:
                jsons = kvant_lib.change_balance(amount, key, for_what, self.root.ids.login.text, self.root.ids.password.text)
                print(json)
                res = requests.post(url=f"{url}/execute", data=jsons.encode("utf-8"))
                # print(res.text)
                print(res.status_code)
        # self.send_message('Начислено')



if __name__ == "__main__":
    MoneyTest().run()
