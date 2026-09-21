import sqlite3
from day import Day


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
        status = row[2]
        start_work = row[3]
        end_work = row[4]

        day = Day(day_id, date, status, start_work, end_work)
        return day

    def get_all_days(self) -> list[Day]:
        """
        Get and return all days.

        Returns:
            A list of all days.
        """
        self.cursor.execute("""
            SELECT day_id,date,status,start_work,end_work FROM days
        """)
        days = []
        rows = self.cursor.fetchall()
        for row in rows:
            day = self.row_to_day(row)
            days.append(day)
        return days

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
