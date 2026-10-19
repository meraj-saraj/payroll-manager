# Payroll Manager

Recording working and non-working days, and calculating overtime and wages.

## Features

- Recording Day
- Updating Day
- Delete Day
- Calculate Wages
- Historical Rate
- Get Report
- Convert Jalali Date to ISO

## Requirements

- Python 3.10+
- jdatetime
- pytest

## Installation

```bash
git clone <repository-url>
cd Payroll-Manager
pip install jdatetime pytest
```

## Usage

Run the application from the project folder:

```bash
python main.py
```

You will see a menu like this:

```
Enter your request:
1.Add a new day
2.Calculate salary for a month
3.Set / Update rate
4.Delete a day
5.Edit a day
6.Show a day by date
7.Show days of a month
8.Show absence days of a month
9.Get report
10.Exit
```

Enter the number of the option you want and follow the prompts.

## Project structure

| File | Description |
|------|-------------|
| main.py | Main file and program execution |
| database.py | Database file and responsible for CRUD operation|
| day.py | Day object file |
| status_work.py | Day status object |
| helper_methodes.py | Methods we need for running program |
| test.py | Testing all program methods |


## Running the tests

```bash
pytest
```

All tests use temporary memory, so there is no need to worry about the actual database file.