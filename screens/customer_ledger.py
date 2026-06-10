from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout

from database.db import db


class CustomerLedgerScreen(MDScreen):

    def on_pre_enter(self):

        self.current_filter = "ALL"

        self.load_data()

    def go_back(self):

        self.manager.current = "home"

    def show_all(self):

        self.current_filter = "ALL"

        self.load_data()

    def show_pending(self):

        self.current_filter = "PENDING"

        self.load_data()

    def show_paid(self):

        self.current_filter = "PAID"

        self.load_data()

    def search_customer(self):

        self.load_data()

    def clear_search(self):

        self.ids.search_field.text = ""

        self.current_filter = "ALL"

        self.load_data()

    def load_data(self):

        self.ids.ledger_container.clear_widgets()

        search_name = (
            self.ids.search_field.text.strip()
        )

        # ==================================
        # SEARCH MODE
        # ==================================

        if search_name:

            all_records = db.get_customer_history(
                search_name
            )

            if not all_records:

                self.ids.summary_label.text = (
                    "No Records Found"
                )

                self.ids.ledger_container.add_widget(
                    MDLabel(
                        text="Customer Not Found",
                        size_hint_y=None,
                        height="40dp"
                    )
                )

                return

            # Summary हमेशा Full History से बनेगी

            summary_minutes = 0
            summary_amount = 0
            summary_paid = 0
            summary_balance = 0

            for row in all_records:

                summary_minutes += int(row[5])
                summary_amount += float(row[6])
                summary_paid += float(row[7])
                summary_balance += float(row[8])

            # Table Filter

            records = all_records.copy()

            if self.current_filter == "PENDING":

                records = [
                    row for row in records
                    if float(row[8]) > 0
                ]

            elif self.current_filter == "PAID":

                records = [
                    row for row in records
                    if float(row[8]) <= 0
                ]

            for index, row in enumerate(records):

                row_widget = MDGridLayout(
                    cols=6,
                    spacing="2dp",
                    size_hint_y=None,
                    height="35dp"
                )

                if index == 0:

                    row_widget.add_widget(
                        MDLabel(
                            text=search_name
                        )
                    )

                else:

                    row_widget.add_widget(
                        MDLabel(
                            text=""
                        )
                    )

                row_widget.add_widget(
                    MDLabel(
                        text=str(row[1]),
                        halign="center"
                    )
                )

                row_widget.add_widget(
                    MDLabel(
                        text=str(row[5]),
                        halign="center"
                    )
                )

                row_widget.add_widget(
                    MDLabel(
                        text=f"₹{row[6]:.0f}",
                        halign="center"
                    )
                )

                row_widget.add_widget(
                    MDLabel(
                        text=f"₹{row[7]:.0f}",
                        halign="center"
                    )
                )

                balance = float(row[8])

                if balance > 0:

                    balance_color = (1, 0.6, 0, 1)      # Orange

                else:

                    balance_color = (0, 1, 0, 1)        # Green

                row_widget.add_widget(
                    MDLabel(
                        text=f"₹{abs(balance):.0f}",
                        theme_text_color="Custom",
                        text_color=balance_color
                    )
                )
                self.ids.ledger_container.add_widget(
                    row_widget
                )

            self.ids.summary_label.text = (
                f"Customer : {search_name}\n"
                f"Entries : {len(all_records)}\n"
                f"Minutes : {summary_minutes}\n"
                f"Amount : ₹{summary_amount:.0f}\n"
                f"Paid : ₹{summary_paid:.0f}\n"
                f"Balance : ₹{summary_balance:.0f}"
            )

            return

        # ==================================
        # NORMAL FILTER MODE
        # ==================================

        if self.current_filter == "PENDING":

            data = db.get_pending_customers()

        elif self.current_filter == "PAID":

            data = db.get_paid_customers()

        else:

            data = db.get_all_customers()

        for row in data:

            row_widget = MDGridLayout(
                cols=6,
                size_hint_y=None,
                height="35dp"
            )

            row_widget.add_widget(
                MDLabel(
                    text=str(row[0])
                )
            )

            row_widget.add_widget(
                MDLabel(text="")
            )

            row_widget.add_widget(
                MDLabel(text="")
            )

            row_widget.add_widget(
                MDLabel(text="")
            )

            row_widget.add_widget(
                MDLabel(text="")
            )

            balance = float(row[1])

            if balance > 0:

                balance_color = (1, 0.6, 0, 1)      # Orange

            else:

                balance_color = (0, 1, 0, 1)        # Green

            row_widget.add_widget(
                MDLabel(
                    text=f"₹{abs(balance):.0f}",
                    theme_text_color="Custom",
                    text_color=balance_color
                )
            )

            self.ids.ledger_container.add_widget(
                row_widget
            )

        self.ids.summary_label.text = (
            f"Customers : {len(data)}"
        )