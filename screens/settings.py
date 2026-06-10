from kivymd.uix.screen import MDScreen
from database.db import db
import shutil
from pathlib import Path 


class SettingsScreen(MDScreen):

    def on_pre_enter(self):

        rate = db.get_setting(
            "default_rate"
        )

        if rate:

            self.ids.rate_input.text = str(
                rate
            )

    def save_rate(self):

        try:

            rate = float(
                self.ids.rate_input.text
            )

            db.set_setting(
                "default_rate",
                rate
            )

            print(
                "DEFAULT RATE SAVED:",
                rate
            )

        except Exception as e:

            print(
                "RATE SAVE ERROR:",
                e
            )

    def go_back(self):

        self.manager.current = "home"

    def export_backup(self):

        try:

            source = Path(
                "water_hisab.db"
            )

            backup = Path(
                "water_hisab_backup.db"
            )

            shutil.copy(
                source,
                backup
            )

            print(
                "BACKUP CREATED"
            )

        except Exception as e:

            print(
                "BACKUP ERROR:",
                e
            )
    def import_backup(self):

        try:

            backup = Path(
                "water_hisab_backup.db"
            )

            target = Path(
                "water_hisab.db"
            )

            if not backup.exists():

                print(
                    "BACKUP FILE NOT FOUND"
                )

                return

            shutil.copy(
                backup,
                target
            )

            print(
                "BACKUP RESTORED"
            )

        except Exception as e:

            print(
                "IMPORT ERROR:",
                e
            )