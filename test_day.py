from database import Database
from day import Day, Status
import pytest
from helper_methodes import *
import jdatetime
from main import create_day_from_user


@pytest.fixture
def db():
    database = Database(":memory:")
    yield database
    database.close()


def test_worked_hours():
    day1 = Day(None, "1405/1/1", "work", "08:00", "16:30")
    assert day1.worked_hours() == 8.5


def test_end_before_start():
    day2 = Day(None, "1405/1/2", "work", "08:00", "06:00")
    with pytest.raises(ValueError):
        day2.worked_hours()


def test_start_and_end_are_None():
    day3 = Day(None, "1405,1,3", "work")
    assert day3.worked_hours() == 0


def test_end_is_None():
    day4 = Day(None, "1405/1/4", "work", "08:00")
    assert day4.worked_hours() == 0


def test_start_work_is_None():
    day5 = Day(None, "1405/1/5", "work", None, "16:00")
    assert day5.worked_hours() == 0


def test_start_equal_end():
    day6 = Day(None, "1405/1/6", "work", "08:00", "08:00")
    with pytest.raises(ValueError):
        day6.worked_hours()


def test_jalali_to_iso():
    jalali = "1405/13/31"
    with pytest.raises(ValueError):
        jalali_to_iso(jalali)


def test_status_day():
    day = Day(None, "2026-09-21", Status.WORK, "08:00", "16:00")
    assert day.status == "work"


def test_status_invalid_value():
    with pytest.raises(ValueError):
        Status("kar")


def test_add_day(db):
    day = Day(None, "2026-09-21", Status.WORK, "08:00", "16:00")
    assert db.add_day(day) == True


def test_get_all_days(db):
    day = Day(None, "2026-09-21", Status.WORK, "08:00", "16:00")
    db.add_day(day)
    assert db.get_all_days() == [
        Day(
            day_id=1,
            date="2026-09-21",
            status=Status.WORK,
            start_work="08:00",
            end_work="16:00",
        )
    ]


def test_type_status(db):
    day = Day(None, "2026-09-21", Status.WORK, "08:00", "16:00")
    db.add_day(day)
    assert type(db.get_all_days()[-1].status) == Status


def test_status(db):
    day = Day(None, "2026-09-21", Status.WORK, "08:00", "16:00")
    db.add_day(day)
    assert db.get_all_days()[-1].status == Status.WORK


def test_get_days_between_uncorrect_format(db):
    with pytest.raises(ValueError):
        db.get_days_between("2026/09/01", "2026/10/01")


def test_get_days_between_reversed_range(db):
    with pytest.raises(ValueError):
        db.get_days_between("2026-10-01", "2026-09-01")


def test_get_days_between_normal(db):
    db.add_day(Day(None, "2026-09-01", Status.WORK, "08:00", "16:00"))
    db.add_day(Day(None, "2026-09-15", Status.WORK, "08:00", "16:00"))
    db.add_day(Day(None, "2026-10-01", Status.WORK, "08:00", "16:00"))
    days = db.get_days_between("2026-09-01", "2026-09-30")
    assert len(days) == 2


def test_jalali_month_range():
    start, end = jalali_month_range(1405, 6)
    assert start < end


def test_jalali_month_range_year_end():
    start, end = jalali_month_range(1405, 12)
    assert start < end





def test_get_valid_year_number(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "1405")
    result = get_valid_year_number()
    assert result == 1405


def test_get_valid_month_number(monkeypatch):
    inputs = iter(["abc", "6"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    result = get_valid_month_number()
    assert result == 6


def test_get_valid_day_number(monkeypatch):
    inputs = iter(["qw", "33", "12"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    result = get_valid_day_number()
    assert result == 12


def test_get_status_from_user(monkeypatch):
    inputs = iter(["9", "2"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    result = get_status_from_user()
    assert result == Status.FRIDAY


def test_get_valid_date(monkeypatch):
    inputs = iter(["1404", "12", "30", "1405", "12", "29"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    result = get_valid_date()
    assert result == "1405/12/29"


def test_create_day_from_user(monkeypatch):
    inputs = iter(["1405", "11", "29", "1", "08:00", "17:00"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    day = create_day_from_user()
    assert day.date == "2027-02-18"
    assert day.status == Status.WORK
    assert day.start_work == "08:00"
    assert day.end_work == "17:00"


def test_create_day_from_user(monkeypatch):
    inputs = iter(["1405", "11", "29", "1", "08:00", "17:00"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    day = create_day_from_user()
    assert day == Day(None, "2027-02-18", Status.WORK, "08:00", "17:00")


def test_add_rate(db):
    effective_date = jalali_to_iso("1405/01/01")
    day_rate = 100
    overtime_rate = 150
    is_add_rate = db.add_rate(effective_date, day_rate, overtime_rate)
    assert is_add_rate == True


def test_get_rate_for_date(db):
    db.add_rate("2026-01-01", 1000000, 200000)
    db.add_rate("2026-09-01", 1200000, 250000)

    assert db.get_rate_for_date("2026-05-10") == (1000000, 200000)
    assert db.get_rate_for_date("2026-12-01") == (1200000, 250000)
    assert db.get_rate_for_date("2025-01-01") is None


def test_get_valid_time2(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "8:00")
    result = get_valid_time("Enter time: ")
    assert result == "08:00"


def test_create_day_from_user_rejects_reversed_times(monkeypatch):
    inputs = iter(["1405", "6", "15", "1", "16:00", "08:00", "08:00", "16:00"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    day = create_day_from_user()
    assert day.start_work == "08:00"
    assert day.status == Status.WORK
    assert day.end_work == "16:00"
    assert day.date == "2026-09-06"


def test_delete_day_by_wrong_date(db):
    day = Day(None, "2026-11-09", Status.WORK, "08:00", "17:00")
    db.add_day(day)
    is_deleted = db.delete_day_by_date("2026-12-09")
    assert is_deleted == False

def test_delete_day_by_right_date(db):
    day = Day(None, "2026-11-09", Status.WORK, "08:00", "17:00")
    db.add_day(day)
    is_deleted = db.delete_day_by_date("2026-11-09")
    assert is_deleted == True
    assert db.get_all_days() == []

def test_update_day(db):
    day = Day(None, "2026-11-09", Status.ABSENCE)
    db.add_day(day)

    is_updated = db.update_day("2026-11-09",Status.WORK,"08:00","17:00")
    assert is_updated == True
    updated_day = db.find_day_by_id(1)
    assert updated_day.day_id == 1
    assert updated_day.date == "2026-11-09"
    assert updated_day.status == Status.WORK
    assert updated_day.start_work == "08:00"
    assert updated_day.end_work == "17:00"

def test_update_day_not_found(db):
    is_updated = db.update_day("2026-01-01",Status.WORK,"08:00","17:00")
    assert is_updated == False

def test_get_status_and_times_work(monkeypatch):
    inputs = iter(["1","08:00","17:00"])
    monkeypatch.setattr("builtins.input",lambda prompt:next(inputs))
    result = get_status_and_times()
    assert result == (Status.WORK,"08:00","17:00")

def test_get_status_and_times_work(monkeypatch):
    monkeypatch.setattr("builtins.input",lambda prompt:"2")
    result = get_status_and_times()
    assert result == (Status.FRIDAY,None,None)


def test_str_magic_method():
    day = Day(None, "2026-11-03", Status.WORK, "08:00", "17:00")
    assert "2026-11-03" in str(day)
    assert "work" in str(day)

def test_get_date_input(monkeypatch):
    inputs = iter(["1405","6","15"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    assert get_date_input() == "2026-09-06"

def test_get_month_range_input(monkeypatch):
    inputs = iter(["1405","06"])
    monkeypatch.setattr("builtins.input",lambda prompt: next(inputs))
    start, end = get_month_range_input() 
    assert start == "2026-08-23"
    assert end == "2026-09-22"

def test_generate_report():
    days = [Day(None, "2026-09-01", Status.WORK, "08:00", "17:00"),Day(None, "2026-09-02", Status.WORK, "08:00", "19:00"),Day(None, "2026-09-03", Status.FRIDAY)]
    report = generate_report(days)
    assert report["work_days"] == 2
    assert report["friday_days"] == 1
    assert report["absence_days"] == 0
    assert report["holiday_days"] == 0
    assert report["total_hours"] == 20
    assert report["overtime_hours"] == 2

def test_calculate_salary():
    days = [
        Day(None, "2026-09-01", Status.WORK, "08:00", "17:00"),
        Day(None, "2026-09-02", Status.WORK, "08:00", "19:00"),
        Day(None, "2026-09-03", Status.FRIDAY),
    ]
    assert calculate_salary(days, day_rate=1000000, overtime_rate=200000) == 2400000

