from typing import List, Tuple
from enum import Enum
import re


class Date:
    """
    Class representing a date.

    Attributes:
        date (str): The date in the format "yyyy-mm-dd".
    """
    def __init__(self, date: str):
        """
        Initializes an instance of the Date class with the provided date.

        Parameters:
        - date (str): The date in the format yyyy-mm-dd.

        Exceptions:
        - Exception: Raises an exception if the provided date does not meet the expected format.

        Example usage:
        >>> d = Date("2023-06-25")
        """
        regex_date = '^20\d{2}-(:?0[1-9]|1[0-2])-\d{2}$'
        if re.compile(regex_date).match(date):
            self.date = date
        else:
            raise Exception('Invalid date, use the format yyyy-mm-dd')


    def __str__(self):
        """
        Returns a string representation of the date.

        Returns:
        - str: A string representing the date.

        Example usage:
        >>> d = Date("2023-06-25")
        >>> print(d)
        Date(date = 2023-06-25)
        """
        return f'Date(date = {self.date})'


    def copy(self):
        """
        Creates a copy of the current instance of the date.

        Returns:
        - Date: A new instance of the Date class with the same date.

        Example usage:
        >>> d1 = Date("2023-06-25")
        >>> d2 = d1.copy()
        >>> d2.date = "2023-06-20"
        >>> print(d1)
        Date(date = 2023-06-25)
        >>> print(d2)
        Date(date = 2023-06-20)
        """
        return Date(self.date)


class Turn:
    """
    Class representing a turn.

    Attributes:
        label (str): The label or name of the turn.
        time_interval (Tuple[int, int]): A tuple representing the start and end time of the turn.
    """
    def __init__(
        self,
        label: str,
        time_interval: Tuple[int,int]
    ):
        """
        Initializes an instance of the Turn class with the provided label and time interval.

        Parameters:
        - label (str): The label or name of the turn.
        - time_interval (Tuple[int, int]): A tuple representing the start and end time of the turn.

        Example usage:
        >>> t = Turns.morning
        """
        self.label = label
        self.time_interval = time_interval


    def __str__(self):
        """
        Returns a string representation of the turn.

        Returns:
        - str: A string representing the turn.

        Example usage:
        >>> t = Turns.morning
        >>> print(t)
        Turn(label = M, time_interval = (9, 12))
        """
        return f'Turn(label = {self.label}, time_interval = {self.time_interval})'


    def copy(self):
        """
        Creates a copy of the current instance of the turn.

        Returns:
        - Turn: A new instance of the Turn class with the same label and time interval.

        Example usage:
        >>> t1 = Turns.morning
        >>> t2 = t1.copy()
        >>> t2.time_interval = (9, 10)
        >>> print(t1)
        Turn(label = M, time_interval = (9, 12))
        >>> print(t2)
        Turn(label = M, time_interval = (9, 10))
        """
        return Turn(self.label, self.time_interval)

# TODO: Create turns from excel file
class Turns(Enum):
    """
    Enumeration representing different turns.
    """
    full = Turn(label='C', time_interval=(8,20))
    morning = Turn(label='M', time_interval=(8,14))
    afternoon = Turn(label='T', time_interval=(14,20))
    night = Turn(label='N', time_interval=(20,8))
    off = Turn(label='L', time_interval=(8,20))

# TODO: Create Workplaces from excel file
class Workplaces(Enum):
    """
    Enumeration representing different workplaces.
    """
    nursing = 'E'
    emergency = 'U'


class WorkspaceNeeds:
    """
    Class representing workspace needs.

    Attributes:
        time_interval (Tuple[int, int]): A tuple representing the start and end time of the workspace needs.
        dates (List[Date]): A list of Date objects representing the dates within the workspace needs.
        requirement (int): The requirement value for the workspace needs.
    """
    def __init__(
        self,
        time_interval: Tuple[int,int],
        dates: List[Date],
        requirement: int
    ):
        """
        Initializes an instance of the WorkspaceNeeds class with the provided time interval, list of dates, and requirement.

        Parameters:
        - time_interval (Tuple[int, int]): A tuple representing the start and end time of the workspace needs.
        - dates (List[Date]): A list of Date objects representing the dates within the workspace needs.
        - requirement (int): The requirement value for the workspace needs.

        Example usage:
        >>> wn = WorkspaceNeeds((8, 20), [Date("2023-06-25"), Date("2023-06-26")], 3)
        """
        self.time_interval = time_interval
        self.dates = dates
        self.requirement = requirement


    def __str__(self):
        """
        Returns a string representation of the workspace needs.

        Returns:
        - str: A string representing the workspace needs.

        Example usage:
        >>> wn = WorkspaceNeeds((8, 20), [Date("2023-06-25"), Date("2023-06-26")], 3)
        >>> print(wn)
        WorkspaceNeeds(time_interval = (8, 20), dates = [Date(date = 2023-06-25), Date(date = 2023-06-26)], requirement = 3)
        """
        return f'WorkspaceNeeds(time_interval = {self.time_interval}, dates = {[d.date for d in self.dates]}, requirement = {self.requirement})'


    def copy(self):
        """
        Creates a copy of the current instance of the workspace needs.

        Returns:
        - WorkspaceNeeds: A new instance of the WorkspaceNeeds class with the same time interval, copied dates, and requirement.

        Example usage:
        >>> wn1 = WorkspaceNeeds((8, 20), [Date("2023-06-25"), Date("2023-06-26")], 3)
        >>> wn2 = wn1.copy()
        >>> wn2.time_interval = (9, 10)
        >>> print(wn1)
        WorkspaceNeeds(time_interval = (8, 20), dates = [Date(date = 2023-06-25), Date(date = 2023-06-26)], requirement = 3)
        >>> print(wn2)
        WorkspaceNeeds(time_interval = (9, 10), dates = [Date(date = 2023-06-25), Date(date = 2023-06-26)], requirement = 3)
        """
        return WorkspaceNeeds(
            time_interval = self.time_interval,
            dates = [d.copy() for d in self.dates],
            requirement = self.requirement
        )


class Workday:
    """
    Class representing a workday.

    Attributes:
        turn (Turn): The turn for the workday.
        date (Date): The date for the workday.
    """
    def __init__(
        self,
        turn: Turns,
        date: Date
    ):
        """
        Initializes an instance of the Workday class with the provided turn and date.

        Parameters:
        - turn (Turns): The turn for the workday, represented by a member of the Turns enumeration.
        - date (Date): The date for the workday, represented by a Date object.

        Example usage:
        >>> wd = Workday(Turns.full, Date("2023-06-25"))
        """
        self.turn = turn
        self.date = date


    def __str__(self):
        """
        Returns a string representation of the workday.

        Returns:
        - str: A string representing the workday.

        Example usage:
        >>> wd = Workday(Turns.full, Date("2023-06-25"))
        >>> print(wd)
        Workday(turn = Turn(label = C, time_interval = (8, 20)), date = Date(date = 2023-06-25))
        """
        return f'Workday(turn = {str(self.turn)}, date = {str(self.date)})'


    def copy(self):
        """
        Creates a copy of the current instance of the workday.

        Returns:
        - Workday: A new instance of the Workday class with the same turn and copied date.

        Example usage:
        >>> wd1 = Workday(Turns.full, Date("2023-06-25"))
        >>> wd2 = wd1.copy()
        >>> wd2.date = Date("2023-06-26")
        >>> print(wd1)
        Workday(turn = Turn(label = C, time_interval = (8, 20)), date = Date(date = 2023-06-25))
        >>> print(wd2)
        Workday(turn = Turn(label = C, time_interval = (8, 20)), date = Date(date = 2023-06-26))
        """
        return Workday(
            turn = self.turn,
            date = self.date.copy()
        )


class Absence:
    """
    Class representing an absence.

    Attributes:
        date (Date): The date of the absence.
        time_interval (Tuple[int, int]): A tuple representing the start and end time of the absence.
    """
    def __init__(
        self,
        date: Date,
        time_interval: Tuple[int,int]
    ):
        """
        Initializes an instance of the Absence class with the provided date and time interval.

        Parameters:
        - date (Date): The date of the absence, represented by a Date object.
        - time_interval (Tuple[int, int]): A tuple representing the start and end time of the absence.

        Example usage:
        >>> absence = Absence(Date("2023-06-25"), (9, 12))
        """
        self.date = date
        self.time_interval = time_interval


    def __str__(self):
        """
        Returns a string representation of the absence.

        Returns:
        - str: A string representing the absence.

        Example usage:
        >>> absence = Absence(Date("2023-06-25"), (9, 12))
        >>> print(absence)
        Absence(date = Date(date = 2023-06-25), time_interval = (9, 12))
        """
        return f'Absence(date = {str(self.date)}, time_interval = {self.time_interval})'


    def copy(self):
        """
        Creates a copy of the current instance of the absence.

        Returns:
        - Absence: A new instance of the Absence class with the same date and time interval.

        Example usage:
        >>> absence1 = Absence(Date("2023-06-25"), (9, 12))
        >>> absence2 = absence1.copy()
        >>> absence2.time_interval = (9, 10)
        >>> print(absence1)
        Absence(date = Date(date = 2023-06-25), time_interval = (9, 12))
        >>> print(absence2)
        Absence(date = Date(date = 2023-06-25), time_interval = (9, 10))
        """
        return Absence(
            date = self.date.copy(),
            time_interval = self.time_interval
        )
