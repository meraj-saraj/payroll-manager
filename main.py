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
        print("6.Show a day by date")
        print("7.Show days of a month")
        print("8.Show absence days of a month")
        print("9.Get report")
        print("10.Exit")
        choice = input(">>> ")
        if choice == "1":
            day = create_day_from_user()
            is_added = db.add_day(day)
            if is_added:
                print("Day was added.")
            else:
                print("Error : The day was not added.")
            

        elif choice == "2":
            start, end = get_month_range_input()
            days = db.get_days_between(start,end)
            rate = db.get_rate_for_date(start)
            if rate is None : 
                print("No rate has been set yet.")
            else:
                day_rate ,overtime_rate = rate
                salary = calculate_salary(days,day_rate,overtime_rate)
                print(f"Salary : {salary}")

        elif choice == "3":
            effective_date = get_date_input()
            day_rate = get_valid_positive_number("day_rate")
            overtime_rate = get_valid_positive_number("overtime_rate")
            is_added = db.add_rate(effective_date,day_rate,overtime_rate)
            if is_added:
                print("Rate updated successfully.")
            else:
                print("Error: this date already has a rate.")

        elif choice == "4":
            date = get_date_input()
            is_deleted = db.delete_day_by_date(date)
            if is_deleted:
                print("Delete successfully.")
            else:
                print("The day not found.")

        elif choice == "5":
            date = get_date_input()
            status,start_work,end_work = get_status_and_times()
            is_updated = db.update_day(date,status,start_work,end_work)
            if is_updated:
                print("Day updated.")
            else:
                print("No day found with that date.")

        elif choice == "6":
            date = get_date_input()
            days = db.get_days_between(date, date)
            if days:
                print(days[0])
            else:
                print("No day found with that date.")

        elif choice == "7":
            start, end = get_month_range_input()
            days = db.get_days_between(start, end)
            if not days:
                print("No days found in this range.")
            else:
                show_days(days)

        elif choice == "8":
            start, end = get_month_range_input()
            days = db.get_days_between(start, end)
            absences = [day for day in days if day.status == Status.ABSENCE]
            if not absences:
                print("No absences found in this range.")
            else:
                show_days(absences)

        elif choice == "9":
            print("Enter start date")
            start = get_date_input()
            print("Enter end date")
            end = get_date_input()
            try:
                days = db.get_days_between(start,end)
                report = generate_report(days)
                print(f"Work days: {report['work_days']}")
                print(f"Friday days: {report['friday_days']}")
                print(f"Holiday days: {report['holiday_days']}")
                print(f"Absence days: {report['absence_days']}")
                print(f"Total hours: {report['total_hours']}")
                print(f"Overtime hours: {report['overtime_hours']}")
                rate = db.get_rate_for_date(start)
                if rate is not None:
                    day_rate, overtime_rate = rate
                    salary = calculate_salary(days,day_rate,overtime_rate)
                    print(f"Salary: {salary}")
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "10":
            print("Exit...")
            break

        else:
            print("Invalid request.")
            
    db.close()




if __name__ == "__main__":
    main()