import sqlite3
from day import Day
from status_work import Status
from datetime import date


class Database:
    """Represent a database."""

    def __init__(self, file_name: str) -> None:
        """
        Manage database.

        Args:
            file_name: The database file name.

        """
        self.file_name = file_name
        self.connection = sqlite3.connect(self.file_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def close(self) -> None:
        """
        Close the database.
        """
        self.connection.close()

    def create_tables(self) -> None:
        """Create database tables."""

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS days(
            day_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL,
            start_work TEXT,
            end_work TEXT
            )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS rates(
        rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
        effective_date TEXT NOT NULL UNIQUE,
        day_rate REAL NOT NULL,
        overtime_rate REAL NOT NULL
        )
        """)
        self.connection.commit()

    def add_day(self, day: Day) -> bool:
        """
        Add a day object to the days tables.

        Args:
            day: A day object.

        Returns:
            True if day was added; otherwise, False.
        """
        try:
            self.cursor.execute(
                """
            INSERT INTO days(
            date,status,start_work,end_work)VALUES(?,?,?,?)
            """,
                (day.date, day.status, day.start_work, day.end_work),
            )
            day.day_id = self.cursor.lastrowid
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def row_to_day(self, row: tuple) -> Day:
        """
        Create a Day object.

        Args:
            row: A tuple from columns of days table.

        Returns:
            A Day object.
        """
        day_id = row[0]
        date = row[1]
        status = Status(row[2])
        start_work = row[3]
        end_work = row[4]

        day = Day(day_id, date, status, start_work, end_work)
        return day

    def rows_to_list(self,rows:list[tuple])->list[Day]:
        """
        Create a days list.

        Args:
            rows: A list of tuples.
        
        Returns:
            A list of Day objects.
        """
        days = []
        for row in rows:
            day = self.row_to_day(row)
            days.append(day)
        return days

    def get_all_days(self) -> list[Day]:
        """
        Get and return all days.

        Returns:
            A list of all days.
        """
        self.cursor.execute("""
            SELECT day_id,date,status,start_work,end_work FROM days
        """)
        rows = self.cursor.fetchall()
        return self.rows_to_list(rows)


    def find_day_by_id(self, day_id: int) -> Day | None:
        """
        Find day by ID.

        Args:
            day_id: The day Id.

        Returns:
            The Day object if found; otherwise, None.
        """
        self.cursor.execute(
            """
        SELECT day_id,date,status,start_work,end_work FROM days WHERE day_id = ?
        """,
            (day_id,),
        )

        row = self.cursor.fetchone()
        if not row:
            return None
        return self.row_to_day(row)

    def get_days_between(self,start_day:str,end_day:str)->list[Day]:
        """
        Finding and return the days between two dates.

        Args:
            start_day: The start day date.
            end_day: The end day date.

        Raises:
            ValueError: If the date format is not correct.
            ValueError: If the start day is after end day.

        Returns:
            A list of days.
        """
        try:
            date.fromisoformat(start_day)
            date.fromisoformat(end_day)
        except ValueError:
            raise ValueError("The date format is not correct.")
        
        if start_day > end_day:
            raise ValueError("The start day can not be after end day")
        
        self.cursor.execute("""
        SELECT day_id,date,status,start_work,end_work FROM days WHERE date BETWEEN ? AND ?
        """,
        (start_day,end_day)
        )
        rows = self.cursor.fetchall()
        return self.rows_to_list(rows)

    def add_rate(self,effective_date:str,day_rate: float,overtime_rate: float)-> bool:
        """
        Add a new rate entry.

        Args:
            effective_date: The date this rate become effective (ISO format).
            day_rate: The daily rate.
            overtime_rate: The overtime hourly rate.

        Returns:
            True if added; otherwise, False.
        """
        try:
            self.cursor.execute("""
            INSERT INTO rates(
            effective_date, day_rate, overtime_rate)
            VALUES (?,?,?)
            """,
            (effective_date, day_rate, overtime_rate),
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_rate_for_date(self,date:str)-> tuple [float, float] | None:
        """
        
        """
        self.cursor.execute("""
        SELECT day_rate,overtime_rate FROM rates
        WHERE effective_date <= ? 
        ORDER BY  effective_date DESC
        LIMIT 1
        """,
        (date,),
        )
        row = self.cursor.fetchone()
        if not row:
            return None
        return row[0],row[1]
