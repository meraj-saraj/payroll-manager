import jdatetime
from datetime import datetime
from day import Day
from status_work import Status

def jalali_to_iso(jalali: str) -> str:
    """
    Converting Solar Hijri date to Gregorian date.

    Args:
        jalali: The Hijri date.

    Returns:
        A string Gregrian date.
    """
    y, m, d = jalali.split("/")
    year, month, day = int(y), int(m), int(d)
    g_date = jdatetime.date(year, month, day)
    return g_date.togregorian().isoformat()


def jalali_month_range(year: int, month: int) -> tuple[str, str]:
    """
    Return the Gregrian ISO start and end dates of a jalali month.

    Args:
        year: Jalali year.
        month: Jalali month(1-12)

    Returns:
        A tuple (start_iso, end_iso)
    """
    start = jdatetime.date(year, month, 1)

    if month < 12:
        next_month = jdatetime.date(year, month + 1, 1)

    elif month == 12:
        next_month = jdatetime.date(year + 1, 1, 1)

    end = next_month - jdatetime.timedelta(days=1)

    start_iso = start.togregorian().isoformat()
    end_iso = end.togregorian().isoformat()
    return start_iso, end_iso

def calculate_salary(days: list[Day], day_rate:float, overtime_rate: float)-> float:
    """
    Calculating salary for a specific range of days.

    Args:   
        days: A list of the Day object.
        day_rate: One-day rate.
        overtime_rate: One-hour overtime rate.

    Returns:
        A float number. 
    """
    day_work_nums = 0
    overtime_hours = 0
    for day in days:
        if day.status == Status.WORK:
            day_work_nums += 1
            work_hours = day.worked_hours()
            if work_hours > 9:
                day_overtime_hours = work_hours - 9
                overtime_hours += day_overtime_hours


    days_rate = day_work_nums * day_rate
    overtimes_rate = overtime_hours * overtime_rate 

    return days_rate + overtimes_rate

def get_status_from_user():
    """
    Get status day from user.

    Returns:
        A Enum 'Status'
    """
    options ={
        "1": Status.WORK,
        "2": Status.FRIDAY,
        "3": Status.HOLIDAY,
        "4": Status.ABSENCE
    }
    while True:
        choice = input("Select status_day:\n1.Work\n2.Friday\n3.Holiday\n4.Absence\n>>>")
        if choice in options:
            return options[choice]
        else:
            print("Enter a number between 1 and 4.")

def get_valid_day_number()-> int:
    """
    Get and return a valid day number.

    Returns:
        A valid day number.
    """
    while True:
        day = input("Enter day number: ")
        try:
            day = int(day)
            if  1 <= day <= 31:
                return day
            print("Invalid day number.")
        except ValueError :
            print("The day number must be integer number.")

def get_valid_month_number()->int:
    """
    Get and return a valid month number.

    Returns:
        A valid month number.
    """
    while True:
        month = input("Enter month number: ")
        try:
            month = int(month)
            if 1 <= month <= 12:
                return month
            print("The month number must be a number between 1 and 12.")
        except ValueError:
            print("The month number must be integer number.")

def get_valid_year_number()-> int:
    """
    Get and return a valid year number.
    """
    while True:
        year = input("Enter year number: ")
        try:
            year = int(year)
            if 1000 <= year <= 9999:
                return year
            print("The year number must be a 4 digits number.")
        except ValueError:
            print("The year number must be integer number.") 


def get_valid_date():
    """
    Get and return valid day date.

    Returns:
        A valid day date.
    """
    while True:
        year = get_valid_year_number()
        month = get_valid_month_number()
        day = get_valid_day_number()
        try:
            jdatetime.date(year,month,day)
            return f"{year}/{month}/{day}"
        except ValueError:
            print("Invalid date, try again.")

def get_valid_time(prompt:str)->str:
    """
    Get and return a valid time string in HH:MM format.

    Args:
        prompt: The message shown to the user.

    Returns:
        A valid time string.
    """
    while True:
        time_str = input(prompt)
        try:
            datetime.strptime(time_str, "%H:%M")
            return time_str
        except ValueError:
            print("Invalid time format. Use HH:MM")