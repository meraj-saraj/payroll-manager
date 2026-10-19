from dataclasses import dataclass
from datetime import datetime
from status_work import Status

@dataclass
class Day:
    """Represent a day."""

    day_id: int | None
    date: str
    status: Status
    start_work: str | None = None
    end_work: str | None = None

    def worked_hours(self) -> float:
        """
        Calculation of working hours.

        Raises:
            ValueError: If the start_work and the end_work is same.
            ValueError: If the start_work is after the end_work.

        Returns:
            A decimal value representing working hours.
        """
        if self.start_work is not None and self.end_work is not None:
            start = datetime.strptime(self.start_work,"%H:%M")
            end = datetime.strptime(self.end_work,"%H:%M")
            hours = (end - start).total_seconds()/3600
            if hours > 0:
                return hours
            elif hours == 0:
                raise ValueError("The start_work and end_work can not be same.")
            else:
                raise ValueError("The start_work is after end_work.")
        return 0.0

    def __str__ (self):
        """
        Return a human_readabale representation of the day.

        Returns:
            A formatted string.
        """
        lines = [f"Date: {self.date}", f"Status: {self.status.value}"]
        if self.status == Status.WORK:
            lines.append(f"Start: {self.start_work}")
            lines.append(f"End: {self.end_work}")
            lines.append(f"Worked hours: {self.worked_hours()}")
        return "\n".join(lines)

