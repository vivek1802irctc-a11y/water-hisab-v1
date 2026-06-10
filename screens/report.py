from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from database.db import db
from datetime import datetime
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout   

class ReportScreen(MDScreen):

    def on_pre_enter(self):

        self.load_all_report()

    def go_back(self):

        self.manager.current = "home"

    def update_summary_cards(
        self,
        income,
        pending,
        expense
    ):

        profit = income - expense

        self.ids.income_label.text = (
            f"₹ {income:.0f}"
        )

        self.ids.pending_label.text = (
            f"₹ {pending:.0f}"
        )

        self.ids.expense_label.text = (
            f"₹ {expense:.0f}"
        )

        self.ids.profit_label.text = (
            f"₹ {profit:.0f}"
        )


    def load_pending_data(
        self,
        data
    ):

        self.ids.pending_container.clear_widgets()

        if not data:

            self.ids.pending_container.add_widget(
                MDLabel(
                    text="No Pending Customers"
                )
            )

            return

        for row in data:

            self.ids.pending_container.add_widget(
                MDLabel(
                    text=f"{row[0]}    ₹ {float(row[1]):.0f}",
                    size_hint_y=None,
                    height="40dp"
                )
            )


    def load_all_report(self):

        income = db.get_total_income()

        pending = db.get_total_pending()

        expense = db.get_total_expense()

        self.update_summary_cards(
            income,
            pending,
            expense
        )

        self.load_pending_data(
            db.get_pending_customers()
        )

    def show_all_report(self):
        self.load_all_report()
        print("ALL REPORT")

    def show_date_report(self):

        self.date_input = MDTextField(
            hint_text="DD-MM-YYYY"
        )

        self.date_dialog = MDDialog(
            title="Enter Date",
            type="custom",
            content_cls=self.date_input,
            buttons=[
                MDRaisedButton(
                    text="APPLY",
                    on_release=lambda x:
                    self.apply_date_filter()
                )
            ]
        )

        self.date_dialog.open()

    def show_month_report(self):
        self.load_month_report()

        print("MONTH REPORT")

    def show_range_report(self):

        form = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="120dp"
        )

        self.from_date_input = MDTextField(
            hint_text="From Date (DD-MM-YYYY)"
        )

        self.to_date_input = MDTextField(
            hint_text="To Date (DD-MM-YYYY)"
        )

        form.add_widget(
            self.from_date_input
        )

        form.add_widget(
            self.to_date_input
        )

        self.range_dialog = MDDialog(
            title="Select Date Range",
            type="custom",
            content_cls=form,
            buttons=[
                MDRaisedButton(
                    text="APPLY",
                    on_release=lambda x:
                    self.apply_range_filter()
                )
            ]
        )

        self.range_dialog.open()
        
    def load_pending_customers(self):

        self.ids.pending_container.clear_widgets()

        data = db.get_pending_customers()

        if not data:

            self.ids.pending_container.add_widget(
                MDLabel(
                    text="No Pending Customers"
                )
            )

            return

        for row in data:

            name = str(row[0])

            amount = float(row[1])

            self.ids.pending_container.add_widget(
                MDLabel(
                    text=f"{name}    ₹ {amount:.0f}",
                    size_hint_y=None,
                    height= "40dp"
                )
            )    

    
    def load_month_report(self):

        today = datetime.now()

        month = today.month
        year = today.year

        records = db.get_records_this_month(
            month,
            year
        )

        expenses = db.get_expenses_this_month(
            month,
            year
        )

        pending_customers = (
            db.get_pending_customers_this_month(
                month,
                year
            )
        )

        income = 0
        pending = 0
        expense = 0

        for row in records:

            income += float(row[6])
            pending += float(row[8])

        for row in expenses:

            expense += float(row[3])

        self.update_summary_cards(
            income,
            pending,
            expense
        )

        self.load_pending_data(
            pending_customers
        )

    def load_date_report(
        self,
        selected_date
    ):

        income, pending = (
            db.get_income_pending_by_date(
                selected_date
            )
        )

        expense = (
            db.get_expense_total_by_date(
                selected_date
            )
        )

        self.update_summary_cards(
            income,
            pending,
            expense
        )

        self.load_pending_data(
            db.get_pending_customers_by_date(
                selected_date
            )
        )

    def apply_date_filter(self):

        selected_date = (
            self.date_input.text.strip()
        )

        if not selected_date:

            return
        
        selected_date = self.date_input.text.strip()

        try:
            datetime.strptime(
                selected_date,
                "%d-%m-%Y"
            )
        except:

            error_dialog = MDDialog(
                title="Invalid Date",
                text="Please enter date in DD-MM-YYYY format",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=lambda x:
                        error_dialog.dismiss()
                    )
                ]
            )

            error_dialog.open()
            return

        self.date_dialog.dismiss()

        self.load_date_report(
            selected_date
        )

        print(
            "DATE REPORT:",
            selected_date
        )

    def load_range_report(
        self,
        from_date,
        to_date
    ):

        records = db.get_records_between_dates(
            from_date,
            to_date
        )

        expenses = db.get_expenses_between_dates(
            from_date,
            to_date
        )

        pending_customers = (
            db.get_pending_customers_between_dates(
                from_date,
                to_date
            )
        )

        income = 0
        pending = 0
        expense = 0

        for row in records:

            income += float(row[6])
            pending += float(row[8])

        for row in expenses:

            expense += float(row[3])

        self.update_summary_cards(
            income,
            pending,
            expense
        )

        self.load_pending_data(
            pending_customers
        )    
    def apply_range_filter(self):

        from_date = (
            self.from_date_input.text.strip()
        )

        to_date = (
            self.to_date_input.text.strip()
        )

        if not from_date or not to_date:

            return
        
        try:

            datetime.strptime(
                from_date,
                "%d-%m-%Y"
            )

            datetime.strptime(
                to_date,
                "%d-%m-%Y"
            )

        except:

            error_dialog = MDDialog(
                title="Invalid Date",
                text="Please enter valid dates in DD-MM-YYYY format",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=lambda x:
                        error_dialog.dismiss()
                    )
                ]
            )

            error_dialog.open()
            return

        self.range_dialog.dismiss()

        self.load_range_report(
            from_date,
            to_date
        )

        print(
            "RANGE REPORT:",
            from_date,
            "TO",
            to_date
        )    