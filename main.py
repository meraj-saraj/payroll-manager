from helper_methodes import *
from database import Database


def create_day_from_user()->Day:
    """
    Build a Day object from user input.

    Returns:
        A new Day object.
    """
    jalali_date = get_valid_date()
    date = jalali_to_iso(jalali_date)
    status,start_work,end_work = get_status_and_times()

    return Day(None,date,status,start_work,end_work)


def main():
    db = Database("payroll.db")
    while True:
        print("Enter your request: ")
        print("1.Add a new day")
        print("2.Calculate salary for a month")
        print("3.Set / Update rate")
        print("4.Delete a day")
        print("5.Edit a day")
        print("6.Exit")
        choice = input(">>> ")
        if choice == "1":
            day = create_day_from_user()
            is_added = db.add_day(day)
            if is_added:
                print("Day was added.")
            else:
                print("Error : The day was not added.")
            

        elif choice == "2":
            year = get_valid_year_number()
            month = get_valid_month_number()
            start , end = jalali_month_range(year, month)
            days = db.get_days_between(start,end)
            rate = db.get_rate_for_date(start)
            if rate is None : 
                print("No rate has been set yet.")
            else:
                day_rate ,overtime_rate = rate
                salary = calculate_salary(days,day_rate,overtime_rate)
                print(f"Salary : {salary}")

        elif choice == "3":
            jalali_date = get_valid_date()
            effective_date = jalali_to_iso(jalali_date)
            day_rate = get_valid_positive_number("day_rate")
            overtime_rate = get_valid_positive_number("overtime_rate")
            is_added = db.add_rate(effective_date,day_rate,overtime_rate)
            if is_added:
                print("Rate updated successfully.")
            else:
                print("Error: this date already has a rate.")

        elif choice == "4":
            jalali_date = get_valid_date()
            date = jalali_to_iso(jalali_date)
            is_deleted = db.delete_day_by_date(date)
            if is_deleted:
                print("Delete successfully.")
            else:
                print("The day not found.")

        elif choice == "5":
            jalali_date = get_valid_date()
            date = jalali_to_iso(jalali_date)
            status,start_work,end_work = get_status_and_times()
            is_updated = db.update_day(date,status,start_work,end_work)
            if is_updated:
                print("Day updated.")
            else:
                print("No day found with that date.")
        elif choice == "6":
            print("Exit...")
            break

        else:
            print("Invalid request.")
            
    db.close()




if __name__ == "__main__":
    main()