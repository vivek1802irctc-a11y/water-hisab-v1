from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton

import calendar
from datetime import datetime

import app_state
from database.db import db


class HomeScreen(MDScreen):

    def on_pre_enter(self):

        if not hasattr(self, "current_date"):
            self.current_date = datetime.now()

        self.load_dashboard()
        self.generate_calendar()

    def load_dashboard(self):

        pending = db.get_total_pending()

        income = db.get_total_income()

        expense = db.get_total_expense()

        profit = income - expense

        self.ids.pending_label.text = (
            f"₹ {pending:.0f}"
        )

        self.ids.profit_label.text = (
            f"₹ {profit:.0f}"
        )

        if profit >= 0:

            self.ids.profit_label.text_color = (
                [0, 1, 0, 1]
            )

        else:

            self.ids.profit_label.text_color = (
                [1, 0, 0, 1]
            )

    def change_month(
        self,
        offset
    ):

        month = (
            self.current_date.month + offset
        )

        year = (
            self.current_date.year
            + (month - 1) // 12
        )

        month = (
            (month - 1) % 12
        ) + 1

        self.current_date = datetime(
            year,
            month,
            1
        )

        self.generate_calendar()

    def generate_calendar(self):

        if "calendar_grid" not in self.ids:
            return

        self.ids.month_label.text = (
            self.current_date.strftime(
                "%B %Y"
            )
        )

        self.ids.calendar_grid.clear_widgets()

        days_header = [
            "Su",
            "Mo",
            "Tu",
            "We",
            "Th",
            "Fr",
            "Sa"
        ]

        for day_name in days_header:

            btn = MDRaisedButton(
                text=day_name,
                disabled=True,
                size_hint=(1, None),
                height="35dp"
            )

            self.ids.calendar_grid.add_widget(
                btn
            )

        first_day = calendar.monthrange(
            self.current_date.year,
            self.current_date.month
        )[0]

        for _ in range(
            (first_day + 1) % 7
        ):

            self.ids.calendar_grid.add_widget(
                MDRaisedButton(
                    text="",
                    disabled=True,
                    opacity=0,
                    size_hint=(1, None),
                    height="35dp"
                )
            )

        cal = calendar.Calendar()

        for day in cal.itermonthdates(
            self.current_date.year,
            self.current_date.month
        ):

            if (
                day.month
                ==
                self.current_date.month
            ):

                btn = MDRaisedButton(
                    text=str(day.day),
                    size_hint=(1, None),
                    height="35dp"
                )

                current_date_str = (
                    day.strftime(
                        "%d-%m-%Y"
                    )
                )

                if (
                    current_date_str
                    ==
                    app_state.selected_date
                ):

                    btn.md_bg_color = (
                        [0, 0.5, 1, 1]
                    )
                else:
                    btn.md_bg_color = (
                        [0.25, 0.25, 0.25, 1]
                    )
                

                btn.bind(
                    on_release=lambda x,
                    d=current_date_str:
                    self.select_date(d)
                )

                self.ids.calendar_grid.add_widget(
                    btn
                )

    def select_date(
        self,
        date_str
    ):

        app_state.selected_date = (
            date_str
        )

        print(
            "Selected Date :",
            date_str
        )

        self.generate_calendar()

        self.manager.current = (
            "customer"
        )

    def open_expense_screen(self):

        self.manager.current = (
            "expense"
        )