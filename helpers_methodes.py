import jdatetime
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
