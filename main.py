from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import NoTransition

from screens.home import HomeScreen
from screens.customer import CustomerScreen
from screens.expense import ExpenseScreen
from screens.report import ReportScreen
from screens.settings import SettingsScreen
from screens.customer_ledger import CustomerLedgerScreen


selected_date = ""


class WindowManager(ScreenManager):
    pass


class WaterHisabApp(MDApp):

    def build(self):

        self.theme_cls.theme_style = "Dark"

        Builder.load_file("kv/home.kv")
        Builder.load_file("kv/customer.kv")
        Builder.load_file("kv/expense.kv")
        Builder.load_file("kv/report.kv")
        Builder.load_file("kv/settings.kv")
        Builder.load_file("kv/customer_ledger.kv")
        sm = WindowManager()
        sm.transition = NoTransition()
        sm.add_widget(
            HomeScreen(name="home")
        )

        sm.add_widget(
            CustomerScreen(name="customer")
        )

        sm.add_widget(
            ExpenseScreen(name="expense")
        )

        sm.add_widget(
            ReportScreen(name="report")
        )

        sm.add_widget(
            SettingsScreen(name="settings")
        )

        sm.add_widget(
            CustomerLedgerScreen(name="customer_ledger")
        )

        return sm


WaterHisabApp().run()