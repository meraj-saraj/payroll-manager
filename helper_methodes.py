import jdatetime
from datetime import datetime
from day import Day
from status_work import Status
STANDARD_HOURS= 9

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

def get_date_input()->str:
    """
    Get jalali date from user and convert to Gregorian ISO.

    Returns:  
        A Gregorian ISO date string.
    """
    jalali_date = get_valid_date()
    date = jalali_to_iso(jalali_date)
    return date

def get_month_range_input()-> tuple[str,str]:
    """
    Get a jalali year and month from user and return  the Gregorian range.

    Returns:
        A tuple (start_iso,end_iso)
    """
    year = get_valid_year_number()
    month = get_valid_month_number()
    start ,end = jalali_month_range(year, month)
    return start, end




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


def get_valid_date()->str:
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
            time_format_str=datetime.strptime(time_str, "%H:%M")
            return time_format_str.strftime("%H:%M")
        except ValueError:
            print("Invalid time format. Use HH:MM")

def get_valid_positive_number(field_name:str)->float:
    """
    Get and return a valid positive number.

    Args:
        field_name: The field name.

    Returns:
        A valid positive number.
    """
    while True:
        number = input(f"Enter {field_name}: ")
        try:
            number = float(number)
            if 0 < number:
                return number
            print(f"THe {field_name} must be a positive number.")
        except ValueError:
            print(f"The {field_name} must be number.")

def get_status_and_times()->tuple[Status,str,str]:
    """
    Get and return day status.

    Returns:
        A tuple.
    """
    status = get_status_from_user()
    if status == Status.WORK:
        while True:
            start_work = get_valid_time("Enter start_work time: ")
            end_work = get_valid_time("Enter end_work time: ")
            if start_work < end_work:
                status_day = status,start_work,end_work
                break
            else:
               print("Start_work must be less than end_work.")
    else:
        status_day = status,None,None
    return status_day

def show_days(days:list[Day])->None:
    """
    Displaying days of list.

    Args:
        days: A days list.
    """
    for day in days:
        print(day)


def generate_report(days: list[Day],standard_hours: float = STANDARD_HOURS)->dict:
    """
    Generate a summary report for a list of days.

    Args:
        days: A list of Day objects to summarieze.

    Returns:
        A dictionary with the report statistics.
    """
    report={
        "work_days":0,
        "friday_days":0,
        "holiday_days":0,
        "absence_days":0,
        "total_hours":0,
        "overtime_hours":0
    }
    for day in days:
        if day.status == Status.FRIDAY:
            report["friday_days"] +=1
        elif day.status == Status.HOLIDAY:
            report["holiday_days"] += 1
        elif day.status == Status.ABSENCE:
            report["absence_days"] += 1
        else:
            report["work_days"] += 1
            try:
                work_hours = day.worked_hours()
                report["total_hours"] += work_hours
                if work_hours > standard_hours:
                    report["overtime_hours"] += work_hours - standard_hours
            except ValueError:
                continue
    return report

def calculate_salary(days: list[Day], day_rate:float, overtime_rate: float, standard_hours = STANDARD_HOURS)-> float:
    """
    Calculating salary for a specific range of days.

    Args:   
        days: A list of the Day object.
        day_rate: One-day rate.
        overtime_rate: One-hour overtime rate.
        standard_hours: Standard working hours per day. Defaults to STANDARD_HOURS.

    Returns:
        A float number. 
    """

    report = generate_report(days,standard_hours)
    days_rate = report["work_days"] * day_rate
    overtimes_rate = report["overtime_hours"] * overtime_rate 

    return days_rate + overtimes_rate