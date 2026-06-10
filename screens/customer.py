from datetime import datetime

import app_state
from database.db import db

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from functools import partial   
from kivymd.uix.pickers import MDTimePicker

class CustomerForm(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.spacing = "10dp"
        self.size_hint_y = None
        self.height = "300dp"

        self.customer_name = MDTextField(
            hint_text="Customer Name"
        )

        self.start_time = MDTextField(
            hint_text="Start Time (08:00 AM)"
        )


        self.end_time = MDTextField(
            hint_text="End Time (09:30 AM)"
        )

        
        saved_rate = db.get_setting(
            "default_rate"
        )

        if not saved_rate:
            saved_rate = "250"

        self.rate = MDTextField(
            hint_text="Rate Per Hour",
            text=str(saved_rate)
        )
        

        self.add_widget(self.customer_name)
        self.add_widget(self.start_time)
        self.add_widget(self.end_time)
        self.add_widget(self.rate)

    def open_start_picker(self, instance, value):

        print("START CLICKED")

        if value:

            time_dialog = MDTimePicker()

            time_dialog.bind(
                time=self.set_start_time
            )

            time_dialog.open()


    def set_start_time(self, instance, time_value):

        hour = time_value.hour
        minute = time_value.minute

        am_pm = "AM"

        if hour >= 12:
            am_pm = "PM"

        if hour > 12:
            hour -= 12

        if hour == 0:
            hour = 12

        self.start_time.text = (
            f"{hour:02d}:{minute:02d} {am_pm}"
        )


    def open_end_picker(self, instance, value):

        if value:

            time_dialog = MDTimePicker()

            time_dialog.bind(
                time=self.set_end_time
            )

            time_dialog.open()


    def set_end_time(self, instance, time_value):

        hour = time_value.hour
        minute = time_value.minute

        am_pm = "AM"

        if hour >= 12:
            am_pm = "PM"

        if hour > 12:
            hour -= 12

        if hour == 0:
            hour = 12

        self.end_time.text = (
            f"{hour:02d}:{minute:02d} {am_pm}"
        )


class CustomerScreen(MDScreen):

    def on_pre_enter(self):

        
        print("Customer Date =", app_state.selected_date)
        self.ids.date_label.text = (
                f"Date : {app_state.selected_date}"
            )
        self.load_records()

    def go_back(self):
        self.manager.current = "home"

    def show_add_customer(self):

        self.form = CustomerForm()

        self.dialog = MDDialog(
            title="Add Customer",
            type="custom",
            content_cls=self.form,
            buttons=[
                MDRaisedButton(
                    text="SAVE",
                    on_release=self.save_customer
                )
            ]
        )

        self.dialog.open()
    def show_error(self, message):

        self.error_dialog = MDDialog(
            title="Invalid Time",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x:
                    self.error_dialog.dismiss()
                )
            ]
        )

        self.error_dialog.open()
    def save_customer(self, *args):

        try:

            name = self.form.customer_name.text.strip()

            start = self.form.start_time.text.strip()

            end = self.form.end_time.text.strip()

            rate = float(self.form.rate.text)

            start_time = datetime.strptime(
                start,
                "%I:%M %p"
            )

            end_time = datetime.strptime(
                end,
                "%I:%M %p"
            )

            if end_time <= start_time:

                self.show_error(
                    "End Time must be greater than Start Time"
                )

                return
            
            minutes = int(
                (end_time - start_time).total_seconds() / 60
            )
            amount = round(
                (minutes / 60) * rate,
                2
            )

            db.add_record(
                app_state.selected_date,
                name,
                start,
                end,
                minutes,
                amount,
                0,
                amount
            )

            self.dialog.dismiss()

            self.load_records()

        except Exception as e:

            print("ERROR :", e)

    def load_records(self):

        if "records_container" not in self.ids:
            return

        self.ids.records_container.clear_widgets()

        print(type(db))
        print(db)
        data = db.get_records_by_date(
            app_state.selected_date
        )

        serial_no = 1

        for row_data in data:

            row = MDGridLayout(
                cols=7,
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
                MDLabel(text=str(row_data[5]))
            )

            row.add_widget(
                MDLabel(text=str(row_data[6]))
            )

            row.add_widget(
                MDLabel(text=str(row_data[7]))
            )

            row.add_widget(
                MDLabel(text=str(row_data[8]))
            )

            action_btn = MDRaisedButton(
                text="⋮",
                size_hint_x=None,
                width="60dp"
            )

            action_btn.bind(
                on_release=partial(
                    self.show_action_menu,
                    row_data
                )
            )

            row.add_widget(action_btn)

            self.ids.records_container.add_widget(
                row
            )

            serial_no += 1


    def show_payment_popup(
        self,
        record_id,
        *args
    ):

        self.payment_field = MDTextField(
            hint_text="Payment Amount"
        )

        self.payment_dialog = MDDialog(
            title="Add Payment",
            type="custom",
            content_cls=self.payment_field,
            buttons=[
                MDRaisedButton(
                    text="SAVE",
                    on_release=lambda x:
                    self.save_payment(
                        record_id
                    )
                )
            ]
        )

        self.payment_dialog.open()

    def save_payment(
        self,
        record_id
    ):

        try:

            amount = float(
                self.payment_field.text
            )

            db.update_payment(
                record_id,
                amount
            )

            self.payment_dialog.dismiss()

            self.load_records()

        except Exception as e:

            print(
                "PAYMENT ERROR:",
                e
            )
        
    def show_action_menu(
        self,
        row_data,
        *args
    ):

        record_id = row_data[0]

        self.action_dialog = MDDialog(
            title=f"{row_data[2]}",
            buttons=[
                MDRaisedButton(
                    text="PAYMENT",
                    on_release=lambda x:
                    self.open_payment_from_action(
                        record_id
                    )
                ),

                MDRaisedButton(
                    text="EDIT",
                    on_release=lambda x:
                    self.edit_record(
                        record_id
                    )
                ),

                MDRaisedButton(
                    text="DELETE",
                    on_release=lambda x:
                    self.delete_record(
                        record_id
                    )
                )
            ]
        )

        self.action_dialog.open()
    
    def open_payment_from_action(
        self,
        record_id
    ):

        self.action_dialog.dismiss()

        self.show_payment_popup(
            record_id
        )


    def edit_record(
        self,
        record_id
    ):

        self.action_dialog.dismiss()

        record = db.get_record_by_id(
            record_id
        )

        self.edit_form = CustomerForm()

        self.edit_form.customer_name.text = str(
            record[2]
        )

        self.edit_form.start_time.text = str(
            record[3]
        )

        self.edit_form.end_time.text = str(
            record[4]
        )

        saved_rate = db.get_setting(
            "default_rate"
        )

        if not saved_rate:
            saved_rate = "250"

        self.edit_form.rate.text = str(
            saved_rate
        )

        self.edit_dialog = MDDialog(
            title="Edit Customer",
            type="custom",
            content_cls=self.edit_form,
            buttons=[
                MDRaisedButton(
                    text="UPDATE",
                    on_release=lambda x:
                    self.update_record(
                        record_id
                    )
                )
            ]
        )

        self.edit_dialog.open()


    def delete_record(
        self,
        record_id
        ):

            self.action_dialog.dismiss()

            self.confirm_delete_dialog = MDDialog(
                title="Delete Customer Record?",
                text="Are you sure you want to delete this record?",
                buttons=[

                    MDRaisedButton(
                        text="NO",
                        on_release=lambda x:
                        self.confirm_delete_dialog.dismiss()
                    ),

                    MDRaisedButton(
                        text="YES",
                        on_release=lambda x:
                        self.final_delete_record(
                            record_id
                        )
                    )
                ]
            )

            self.confirm_delete_dialog.open()


    def final_delete_record(
        self,
        record_id
    ):

        db.delete_record(
            record_id
        )

        self.confirm_delete_dialog.dismiss()

        self.load_records()
    
    def update_record(
        self,
        record_id
    ):

        try:

            name = self.edit_form.customer_name.text.strip()

            start = self.edit_form.start_time.text.strip()

            end = self.edit_form.end_time.text.strip()

            rate = float(
                    self.edit_form.rate.text
                )

            start_time = datetime.strptime(
                start,
                "%I:%M %p"
            )

            end_time = datetime.strptime(
                end,
                "%I:%M %p"
            )

            if end_time <= start_time:

                self.show_error(
                    "End Time must be greater than Start Time"
                )

                return
            
            minutes = int(
                (end_time - start_time).total_seconds() / 60
            )

            amount = round(
                (minutes / 60) * rate,
                2
            )

            record = db.get_record_by_id(
                record_id
            )

            paid = float(record[7])

            balance = amount - paid

            db.update_record(
                record_id,
                name,
                start,
                end,
                minutes,
                amount,
                balance
            )

            self.edit_dialog.dismiss()

            self.load_records()

        except Exception as e:

            print(
                "UPDATE ERROR:",
                e
            )
                