import sqlite3
from pathlib import Path

DB_NAME = "water_hisab.db"


class DatabaseManager:

    def __init__(self):
        self.db_path = Path(DB_NAME)
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_date TEXT,
            customer_name TEXT,
            start_time TEXT,
            end_time TEXT,
            minutes INTEGER,
            amount REAL,
            paid REAL DEFAULT 0,
            balance REAL DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT,
            expense_type TEXT,
            amount REAL,
            notes TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE,
            setting_value TEXT
        )
        """)

        conn.commit()
        conn.close()

    def add_record(
        self,
        record_date,
        customer_name,
        start_time,
        end_time,
        minutes,
        amount,
        paid,
        balance
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO records(
            record_date,
            customer_name,
            start_time,
            end_time,
            minutes,
            amount,
            paid,
            balance
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            record_date,
            customer_name,
            start_time,
            end_time,
            minutes,
            amount,
            paid,
            balance
        ))

        conn.commit()
        conn.close()

    def get_records_by_date(self, record_date):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM records
        WHERE record_date=?
        ORDER BY id ASC
        """, (record_date,))

        data = cursor.fetchall()

        conn.close()

        return data

    def get_setting(self, key):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT setting_value FROM settings WHERE setting_key=?",
            (key,)
        )

        row = cursor.fetchone()

        conn.close()

        return row[0] if row else None

    def set_setting(self, key, value):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO settings(
            setting_key,
            setting_value
        )
        VALUES(?,?)
        ON CONFLICT(setting_key)
        DO UPDATE SET
        setting_value=excluded.setting_value
        """, (key, str(value)))

        conn.commit()
        conn.close()
    
    def update_payment(
        self,
        record_id,
        payment_amount
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT amount, paid
        FROM records
        WHERE id=?
        """, (record_id,))

        row = cursor.fetchone()

        if row:

            amount = float(row[0])

            old_paid = float(row[1])

            new_paid = old_paid + payment_amount

            new_balance = amount - new_paid

            cursor.execute("""
            UPDATE records
            SET paid=?,
                balance=?
            WHERE id=?
            """,
            (
                new_paid,
                new_balance,
                record_id
            ))

        conn.commit()
        conn.close()
    def delete_record(self, record_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM records
        WHERE id=?
        """, (record_id,))

        conn.commit()
        conn.close()
    
    def get_record_by_id(self, record_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM records
        WHERE id=?
        """, (record_id,))

        data = cursor.fetchone()

        conn.close()

        return data

    def update_record(
        self,
        record_id,
        customer_name,
        start_time,
        end_time,
        minutes,
        amount,
        balance
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE records
        SET customer_name=?,
            start_time=?,
            end_time=?,
            minutes=?,
            amount=?,
            balance=?
        WHERE id=?
        """,
        (
            customer_name,
            start_time,
            end_time,
            minutes,
            amount,
            balance,
            record_id
        ))

        conn.commit()
        conn.close()
    
    def add_expense(
        self,
        expense_date,
        expense_type,
        amount,
        notes
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO expenses(
            expense_date,
            expense_type,
            amount,
            notes
        )
        VALUES(?,?,?,?)
        """,
        (
            expense_date,
            expense_type,
            amount,
            notes
        ))

        conn.commit()
        conn.close()

    def get_expenses_by_date(
        self,
        expense_date
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM expenses
        WHERE expense_date=?
        ORDER BY id ASC
        """, (expense_date,))

        data = cursor.fetchall()

        conn.close()

        return data
    def delete_expense(
        self,
        expense_id
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM expenses WHERE id=?",
            (expense_id,)
        )

        conn.commit()
        conn.close()
    
    def get_expense_by_id(
        self,
        expense_id
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM expenses
        WHERE id=?
        """, (expense_id,))

        data = cursor.fetchone()

        conn.close()

        return data


    def update_expense(
        self,
        expense_id,
        expense_type,
        amount,
        notes
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE expenses
        SET expense_type=?,
            amount=?,
            notes=?
        WHERE id=?
        """,
        (
            expense_type,
            amount,
            notes,
            expense_id
        ))

        conn.commit()
        conn.close()

    def get_total_income(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM records
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    def get_total_pending(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COALESCE(SUM(balance),0)
        FROM records
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    def get_total_expense(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM expenses
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    def get_all_expenses(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM expenses
        ORDER BY expense_date DESC, id DESC
        """)

        data = cursor.fetchall()

        conn.close()

        return data


    def get_expenses_this_month(
        self,
        month,
        year
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM expenses
        WHERE substr(expense_date,4,2)=?
        AND substr(expense_date,7,4)=?
        ORDER BY expense_date DESC
        """,
        (
            f"{month:02d}",
            str(year)
        ))

        data = cursor.fetchall()

        conn.close()

        return data


    def get_expenses_between_dates(
        self,
        from_date,
        to_date
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM expenses
        ORDER BY expense_date ASC
        """)

        all_rows = cursor.fetchall()

        conn.close()

        filtered = []

        from datetime import datetime

        start = datetime.strptime(
            from_date,
            "%d-%m-%Y"
        )

        end = datetime.strptime(
            to_date,
            "%d-%m-%Y"
        )

        for row in all_rows:

            if not row[1]:
                continue

            try:

                current = datetime.strptime(
                    row[1],
                    "%d-%m-%Y"
                )

                if start <= current <= end:
                    filtered.append(row)

            except:
                continue

        return filtered
    
    def get_pending_customers(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT customer_name,
            SUM(balance)
        FROM records
        WHERE balance > 0
        GROUP BY customer_name
        ORDER BY SUM(balance) DESC
        """)

        data = cursor.fetchall()

        conn.close()

        return data
    
    def get_pending_customers_by_date(
        self,
        record_date
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT customer_name,
            SUM(balance)
        FROM records
        WHERE balance > 0
        AND record_date=?
        GROUP BY customer_name
        ORDER BY SUM(balance) DESC
        """, (record_date,))

        data = cursor.fetchall()

        conn.close()

        return data
    
    def get_pending_customers_this_month(
        self,
        month,
        year
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT customer_name,
            SUM(balance)
        FROM records
        WHERE balance > 0
        AND substr(record_date,4,2)=?
        AND substr(record_date,7,4)=?
        GROUP BY customer_name
        ORDER BY SUM(balance) DESC
        """,
        (
            f"{month:02d}",
            str(year)
        ))

        data = cursor.fetchall()

        conn.close()

        return data
    
    def get_pending_customers_between_dates(
        self,
        from_date,
        to_date
    ):

        records = self.get_records_between_dates(
            from_date,
            to_date
        )

        customer_data = {}

        for row in records:

            name = row[2]
            balance = float(row[8])

            if balance <= 0:
                continue

            if name not in customer_data:
                customer_data[name] = 0

            customer_data[name] += balance

        result = []

        for name, balance in customer_data.items():

            result.append(
                (name, balance)
            )

        result.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return result
    
    def get_all_records(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM records
        ORDER BY record_date DESC, id DESC
        """)

        data = cursor.fetchall()

        conn.close()

        return data


    def get_records_this_month(
        self,
        month,
        year
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM records
        WHERE substr(record_date,4,2)=?
        AND substr(record_date,7,4)=?
        ORDER BY record_date DESC
        """,
        (
            f"{month:02d}",
            str(year)
        ))

        data = cursor.fetchall()

        conn.close()

        return data
    
    def get_records_between_dates(
        self,
        from_date,
        to_date
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM records
        ORDER BY record_date ASC
        """)

        all_rows = cursor.fetchall()

        conn.close()

        filtered = []

        from datetime import datetime

        start = datetime.strptime(
            from_date,
            "%d-%m-%Y"
        )

        end = datetime.strptime(
            to_date,
            "%d-%m-%Y"
        )

        for row in all_rows:

            if not row[1]:
                continue

            try:

                current = datetime.strptime(
                    row[1],
                    "%d-%m-%Y"
                )

                if start <= current <= end:
                    filtered.append(row)

            except:
                continue

        return filtered

    def get_income_pending_by_date(
        self,
        record_date
    ):

        records = self.get_records_by_date(
            record_date
        )

        income = 0
        pending = 0

        for row in records:

            income += float(row[6])

            pending += float(row[8])

        return income, pending    

    def get_expense_total_by_date(
        self,
        expense_date
    ):

        expenses = self.get_expenses_by_date(
            expense_date
        )

        total = 0

        for row in expenses:

            total += float(row[3])

        return total
    
    def get_customer_history(
        self,
        customer_name
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM records
        WHERE customer_name=?
        ORDER BY record_date ASC
        """, (customer_name,))

        data = cursor.fetchall()

        conn.close()

        return data
    
    def get_paid_customers(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT customer_name,
            SUM(balance)
        FROM records
        GROUP BY customer_name
        HAVING SUM(balance) <= 0
        ORDER BY customer_name ASC
        """)

        data = cursor.fetchall()

        conn.close()

        return data
    def get_all_customers(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT customer_name,
            SUM(balance)
        FROM records
        GROUP BY customer_name
        ORDER BY customer_name ASC
        """)

        data = cursor.fetchall()

        conn.close()

        return data
    
db = DatabaseManager()