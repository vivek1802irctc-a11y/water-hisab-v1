from datetime import datetime

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout

from database.db import db
import app_state


class ExpenseForm(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.spacing = "10dp"
        self.size_hint_y = None
        self.height = "250dp"

        self.expense_type = MDTextField(
            hint_text="Expense Type"
        )

        self.amount = MDTextField(
            hint_text="Amount"
        )

        self.notes = MDTextField(
            hint_text="Notes"
        )

        self.add_widget(self.expense_type)
        self.add_widget(self.amount)
        self.add_widget(self.notes)


class ExpenseScreen(MDScreen):

    def on_pre_enter(self):

        if not hasattr(
            self,
            "filter_mode"
        ):
            self.filter_mode = "ALL"

        self.load_expenses()

    def go_back(self):

        self.manager.current = "home"

    def set_filter_all(self):

        self.filter_mode = "ALL"

        self.load_expenses()

    def set_filter_selected_date(self):

        self.filter_mode = "DATE"

        self.load_expenses()

    def set_filter_this_month(self):

        self.filter_mode = "MONTH"

        self.load_expenses()

    def show_custom_range_popup(self):

        self.from_field = MDTextField(
            hint_text="From Date (DD-MM-YYYY)",
            size_hint_y=None,
            height="60dp"
        )

        self.to_field = MDTextField(
            hint_text="To Date (DD-MM-YYYY)",
            size_hint_y=None,
            height="60dp"
        )

        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="140dp"
        )

        content.add_widget(
            self.from_field
        )

        content.add_widget(
            self.to_field
        )

        self.range_dialog = MDDialog(
            title="Custom Range",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="APPLY",
                    on_release=lambda x:
                    self.apply_custom_range()
                )
            ]
        )

        self.range_dialog.open()

    def apply_custom_range(self):

        from_date = (
            self.from_field.text.strip()
        )

        to_date = (
            self.to_field.text.strip()
        )

        if not from_date or not to_date:

            print(
                "Enter both dates"
            )

            return

        self.filter_mode = "RANGE"

        self.range_from = from_date

        self.range_to = to_date

        self.range_dialog.dismiss()

        self.load_expenses()

    def show_add_expense(self):

        self.form = ExpenseForm()

        self.dialog = MDDialog(
            title="Add Expense",
            type="custom",
            content_cls=self.form,
            buttons=[
                MDRaisedButton(
                    text="SAVE",
                    on_release=self.save_expense
                )
            ]
        )

        self.dialog.open()

    def save_expense(self, *args):

        try:
            print(
                "Expense Date =",
                app_state.selected_date
            )

            
            db.add_expense(
                app_state.selected_date,
                self.form.expense_type.text,
                float(
                    self.form.amount.text
                ),
                self.form.notes.text
            )

            self.dialog.dismiss()

            self.load_expenses()

        except Exception as e:

            print(
                "EXPENSE ERROR:",
                e
            )

    def load_expenses(self):

        self.ids.expense_container.clear_widgets()

        if self.filter_mode == "ALL":

            self.ids.date_label.text = (
                "All Dates"
            )

            data = db.get_all_expenses()

        elif self.filter_mode == "DATE":

            self.ids.date_label.text = (
                app_state.selected_date
            )

            data = db.get_expenses_by_date(
                app_state.selected_date
            )

        elif self.filter_mode == "MONTH":

            now = datetime.now()

            self.ids.date_label.text = (
                "This Month"
            )

            data = db.get_expenses_this_month(
                now.month,
                now.year
            )

        else:

            self.ids.date_label.text = (
                f"{self.range_from} → {self.range_to}"
            )

            data = db.get_expenses_between_dates(
                self.range_from,
                self.range_to
            )

        self.render_rows(data)

    def render_rows(
        self,
        data
    ):

        serial_no = 1

        for row_data in data:
        
            row = MDGridLayout(
                cols=5,
                size_hint_y=None,
                height="40dp",
                spacing="5dp"
            )

            row.add_widget(
                MDLabel(text=str(serial_no))
            )

            row.add_widget(
                MDLabel(text=str(row_data[2]))
            )

            row.add_widget(
                MDLabel(text=str(row_data[3]))
            )

            row.add_widget(
                MDLabel(text=str(row_data[4]))
            )

            action_btn = MDRaisedButton(
                text="⋮",
                size_hint_x=None,
                width="60dp"
            )

            action_btn.bind(
                on_release=lambda x,
                expense=row_data:
                self.show_expense_menu(
                    expense
                )
            )

            row.add_widget(action_btn)

            self.ids.expense_container.add_widget(
                row
            )

            serial_no += 1

    def show_expense_menu(
        self,
        row_data
    ):

        self.expense_menu = MDDialog(
            title=str(row_data[2]),
            buttons=[

                MDRaisedButton(
                    text="EDIT",
                    on_release=lambda x:
                    self.edit_expense(
                        row_data[0]
                    )
                ),

                MDRaisedButton(
                    text="DELETE",
                    on_release=lambda x:
                    self.delete_expense(
                        row_data[0]
                    )
                )
            ]
        )

        self.expense_menu.open()

    def edit_expense(
        self,
        expense_id
    ):

        self.expense_menu.dismiss()

        expense = db.get_expense_by_id(
            expense_id
        )

        self.edit_form = ExpenseForm()

        self.edit_form.expense_type.text = str(
            expense[2]
        )

        self.edit_form.amount.text = str(
            expense[3]
        )

        self.edit_form.notes.text = str(
            expense[4]
        )

        self.edit_dialog = MDDialog(
            title="Edit Expense",
            type="custom",
            content_cls=self.edit_form,
            buttons=[
                MDRaisedButton(
                    text="UPDATE",
                    on_release=lambda x:
                    self.update_expense(
                        expense_id
                    )
                )
            ]
        )

        self.edit_dialog.open()

    def update_expense(
        self,
        expense_id
    ):

        try:

            db.update_expense(
                expense_id,
                self.edit_form.expense_type.text,
                float(
                    self.edit_form.amount.text
                ),
                self.edit_form.notes.text
            )

            self.edit_dialog.dismiss()

            self.load_expenses()

        except Exception as e:

            print(
                "UPDATE EXPENSE ERROR:",
                e
            )

    def delete_expense(
        self,
        expense_id
    ):

        self.expense_menu.dismiss()

        self.confirm_delete_dialog = MDDialog(
            title="Delete Expense?",
            text="Are you sure?",
            buttons=[

                MDRaisedButton(
                    text="NO",
                    on_release=lambda x:
                    self.confirm_delete_dialog.dismiss()
                ),

                MDRaisedButton(
                    text="YES",
                    on_release=lambda x:
                    self.final_delete_expense(
                        expense_id
                    )
                )
            ]
        )

        self.confirm_delete_dialog.open()

    def final_delete_expense(
        self,
        expense_id
    ):

        db.delete_expense(
            expense_id
        )

        self.confirm_delete_dialog.dismiss()

        self.load_expenses()