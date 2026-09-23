from enum import Enum

class Status(str, Enum):
    """Represent the status of a day."""
    WORK = "work"
    FRIDAY = "friday"
    HOLIDAY = "haliday"
    ABSENCE = "absence"