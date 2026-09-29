from helper_methodes import *

def create_day_from_user()->Day:
    """
    Build a Day object from user input.

    Returns:
        A new Day object.
    """
    jalali_date = get_valid_date()
    date = jalali_to_iso(jalali_date)
    status = get_status_from_user()

    if status == Status.WORK:
        start_work = get_valid_time("Enter start_work time: ")
        end_work = get_valid_time("Enter end_work time: ")
    else:
        start_work = None
        end_work = None
    return Day(None,date,status,start_work,end_work)

