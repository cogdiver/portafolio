from typing import List, Tuple
from enum import Enum
import re


class Date:
    def __init__(self, date: str):
        regex_date = '^20\d{2}-(:?0[1-9]|1[0-2])-\d{2}$'
        if re.compile(regex_date).match(date):
            self.date = date
        else:
            raise Exception('Invalid date, use the format yyyy-mm-dd')


    def __str__(self):
        return f'Date(date = {self.date})'


    def copy(self):
        return Date(self.date)


class Turn:
    def __init__(
        self,
        label: str,
        time_interval: Tuple[int,int]
    ):
        self.label = label
        self.time_interval = time_interval


    def __str__(self):
        return f'Turn(label = {self.label}, time_interval = {self.time_interval})'


    def copy(self):
        return Turn(self.label, self.time_interval)


class Turns(Enum):
    corrido = Turn(label='C', time_interval=(8,20))
    mañana = Turn(label='M', time_interval=(8,14))
    tarde = Turn(label='T', time_interval=(14,20))
    noche = Turn(label='N', time_interval=(20,8))
    libre = Turn(label='L', time_interval=(8,20))


class Workplaces(Enum):
    enfermeria = 'E'
    urgencias = 'U'


class WorkspaceNeeds:
    def __init__(
        self,
        time_interval: Tuple[int,int],
        dates: List[Date],
        requirement: int
    ):
        self.time_interval = time_interval
        self.dates = dates
        self.requirement = requirement


    def __str__(self):
        return f'WorkspaceNeeds(time_interval = {self.time_interval}, dates = {[str(d) for d in self.dates]}, requirement = {self.requirement})'


    def copy(self):
        return WorkspaceNeeds(
            time_interval = self.time_interval,
            dates = [d.copy() for d in self.dates],
            requirement = self.requirement
        )


class Workday:
    def __init__(
        self,
        turn: Turns,
        date: Date
    ):
        self.turn = turn
        self.date = date


    def __str__(self):
        return f'Workday(turn = {str(self.turn)}, date = {str(self.date)})'


    def copy(self):
        return Workday(
            turn = self.turn,
            date = self.date.copy()
        )


class Absence:
    def __init__(
        self,
        date: Date,
        time_interval: Tuple[int,int]
    ):
        self.date = date
        self.time_interval = time_interval


    def __str__(self):
        return f'Absence(date = {str(self.date)}, time_interval = {self.time_interval})'


    def copy(self):
        return Absence(
            date = self.date.copy(),
            time_interval = self.time_interval
        )
