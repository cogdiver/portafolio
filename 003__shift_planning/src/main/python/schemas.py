from src.main.python.utils import intervalOverlap, getWorkTime, getIntervals

from functools import reduce
from time import time
import pandas as pd
from typing import List, Dict, Tuple
from enum import Enum
import copy
import re


class Date:
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


class Workplan:
    def __init__(self, plan = {}):
        """
        Initializes a work plan with an optional existing plan.

        Parameters:
        - plan (dict, optional): An optional existing plan to initialize the work plan.
                                 Defaults to an empty dictionary.

        Example usage:
        >>> existing_plan = {'2023-06-26': {'workplace': Workplaces.nursing, 'turn': Turns.morning}}
        >>> wp = Workplan(existing_plan)
        >>> print(wp)
        Workplan({'2023-06-26': {'workplace': 'Workplaces.nursing', 'turn': 'Turns.morning'}})
        """
        self.plan = plan


    def __str__(self):
        """
        Returns a string representation of the work plan.

        Returns:
        - str: A string representation of the work plan.

        Example usage:
        >>> wp = Workplan()
        >>> wp.assing(Date("2023-06-26"), Workplaces.nursing, Turns.morning)
        >>> wp.assing(Date("2023-06-27"), Workplaces.emergency, Turns.afternoon)
        >>> print(wp)
        Workplan({'2023-06-26': {'workplace': 'nursing', 'turn': 'morning'},
                  '2023-06-27': {'workplace': 'emergency', 'turn': 'afternoon'}})
        """
        return f'Workplan({str({d: {k: str(v) for k, v in wd.items()} for d, wd in self.plan.items()})})'


    def copy(self):
        """
        Creates a shallow copy of the work plan.

        Returns:
        - Workplan: A new instance of the Workplan class with a shallow copy of the plan.

        Example usage:
        >>> wp = Workplan()
        >>> wp.assign(Date("2023-06-26"), Workplaces.nursing, Turns.morning)
        >>> wp_copy = wp.copy()
        >>> print(wp_copy)
        Workplan({'2023-06-26': {'workplace': 'Workplaces.nursing', 'turn': 'Turns.morning'}})
        """
        plan = {d: v for d, v in self.plan.items()}
        return Workplan(plan)


    def assing(
        self,
        date: Date,
        workplace: Workplaces,
        turn: Turns
    ):
        """
        Assigns a workplace and turn to a specific date in the work plan.

        Parameters:
        - date (Date): The date to be assigned.
        - workplace (Workplaces): The workplace to be assigned.
        - turn (Turns): The turn to be assigned.

        Example usage:
        >>> wp = Workplan()
        >>> wp.assing(Date("2023-06-26"), Workplaces.nursing, Turns.morning)
        >>> print(wp)
        Workplan({'2023-06-26': {'workplace': 'nursing', 'turn': 'morning'}})
        """
        self.plan[date.date] = {
            'workplace': workplace,
            'turn': turn
        }


class Employee:
    def __init__(
        self,
        name: str,
        work_time: int,
        absences: List[Absence] = [],
        workplan: Workplan = Workplan()
    ):
        """
        Initializes an Employee object with the specified attributes.

        Parameters:
        - name (str): The name of the employee.
        - work_time (int): The total work time of the employee.
        - absences (List[Absence], optional): A list of absences for the employee. Defaults to an empty list.
        - workplan (Workplan, optional): The work plan for the employee. Defaults to an empty Workplan.

        Example usage:
        >>> employee = Employee("John Doe", 40, [Absence(Date("2023-06-25"), (9, 12))])
        """
        self.name = name
        self.work_time = work_time
        self.absences = absences
        self.workplan = workplan


    def __str__(self):
        """
        Returns a string representation of the employee.

        Returns:
        - str: A string representing the employee.

        Example usage:
        >>> employee = Employee("John Doe", 40, [Absence(Date("2023-06-25"), (9, 12))])
        >>> print(employee)
        Employee(name = John Doe,
                 work_time = 40,
                 absences = [Absence(date = Date(date = 2023-06-25))],
                 workplan = {})
        """
        return f'Employee(name = {self.name},' \
                     + f' work_time = {self.work_time},' \
                     + f' absences = {[str(a) for a in self.absences]},' \
                     + f' workplan = {str(self.workplan)})'


    def copy(self):
        """
        Creates a copy of the current instance of the employee.

        Returns:
        - Employee: A new instance of the Employee class with the same name, work time, copied absences, and copied workplan.

        Example usage:
        >>> employee1 = Employee("John Doe", 40, [Absence(Date("2023-06-25"), (9, 12))])
        >>> employee2 = employee1.copy()
        >>> employee2.absences.append(Absence(Date("2023-06-26"), (14, 16)))
        >>> print(employee1)
        Employee(name = John Doe,
                 work_time = 40,
                 absences = [Absence(date = Date(date = 2023-06-25),
                 time_interval = (9, 12))], workplan = {})
        >>> print(employee2)
        Employee(name = John Doe, work_time = 40, absences = [Absence(date = Date(date = 2023-06-25), time_interval = (9, 12)), Absence(date = Date(date = 2023-06-26), time_interval = (14, 16))], workplan = {})
        """
        return Employee(
            name = self.name,
            work_time = self.work_time,
            absences = [a.copy() for a in self.absences],
            workplan = self.workplan.copy()
        )


    def schedule(
        self,
        workplace: Workplaces,
        workday: Workday
    ):
        """
        Schedules a workday for the employee at the specified workplace.

        Parameters:
        - workplace (Workplaces): The workplace where the employee is scheduled to work.
        - workday (Workday): The workday to be scheduled.

        Returns:
        - bool: True if the workday is successfully scheduled, False otherwise.

        Example usage:
        >>> employee = Employee("John Doe", 40, [Absence(Date("2023-06-25"), (9, 12))])
        >>> t1 = Turns.morning
        >>> w1 = Workday(t1, Date("2023-06-26"))
        >>> result = employee.schedule(Workplaces.emergency, w1)
        >>> print(result)
        True
        >>> print(employee.workplan)
        Workplan({'2023-06-26': {'workplace': Workplaces.emergency, 'turn': Turn(label = Morning, time_interval = (9, 12))}})
        """
        if all(
            [
                not intervalOverlap(
                    a.time_interval,
                    workday.turn.value.time_interval
                ) for a in self.absences
                if a.date.date == workday.date.date
            ]
        ):
            self.workplan.assing(workday.date, workplace, workday.turn)
            return True

        else:
            self.workplan.assing(workday.date, workplace, Turns.off)
            return False


    def getTimeOffWork(self):
        """
        Calculates the remaining time off work for the employee.

        Returns:
        - int: The remaining time off work in hours.

        Example usage:
        >>> employee = Employee("John Doe", 40, [Absence(Date("2023-06-25"), (9, 12))])
        >>> t1 = Turns.morning # 6 hours
        >>> w1 = Workday(t1, Date("2023-06-26"))
        >>> employee.schedule(Workplaces.emergency, w1)
        >>> time_off = employee.getTimeOffWork()
        >>> print(time_off)
        34
        """
        intervals = [w['turn'].value.time_interval for _, w in self.workplan.plan.items() if w['turn'] != Turns.off]
        total_work_time = [getWorkTime(start, end) for start, end in intervals]
        time_off_work = self.work_time - reduce(lambda a,b: a+b, total_work_time)

        return time_off_work


    def getWorkplan(self):
        """
        Retrieves the workplan of the employee.

        Returns:
        - List[Dict]: A list of dictionaries representing the work assignment.

        Example usage:
        >>> employee = Employee("John Doe", 40)
        >>> t1 = Turns.morning
        >>> t2 = Turns.afternoon
        >>> w1 = Workday(t1, Date("2023-06-26"))
        >>> w2 = Workday(t2, Date("2023-06-27"))
        >>> employee.schedule(Workplaces.emergency, w1)
        >>> employee.schedule(Workplaces.nursing, w2)
        >>> workplan = employee.getWorkplan()
        >>> print(workplan)
        [{'name': 'John Doe', 'date': '2023-06-26', 'assignment': 'M-U'},
        {'name': 'John Doe', 'date': '2023-06-27', 'assignment': 'T-E'}]
        """
        return [
            {
                'name': self.name,
                **{
                    'date': date,
                    'assignment': "{}-{}".format(
                        w['turn'].value.label,
                        w['workplace'].value
                    )
                }
            } for date, w in self.workplan.plan.items()
        ]


# TODO: Completar metodos
# TODO: Documentar
class Assignment:
    def __init__(self, value = {}):
        self.value = value


    def __str__(self):
        return f'Assignment()'


    def copy(self):
        value = {k: v for k, v in self.value.items()}
        return Assignment(value)


    def assing(self):
        pass


class Workplace:
    def __init__(
        self,
        name: Workplaces,
        capacity: int,
        requirements: List[WorkspaceNeeds],
        assignment: Assignment = Assignment()
    ):
        """
        Initializes a Workplace object.

        Args:
            name (Workplaces): The name of the workplace.
            capacity (int): The capacity of the workplace.
            requirements (List[WorkspaceNeeds]): The requirements of the workplace.
            assignment (Assignment, optional): The assignments made to the workplace. Defaults to an empty Assignment object.
        """
        self.name = name
        self.capacity = capacity
        self.requirements = requirements
        self.assignment = assignment


    def __str__(self):
        """
        Returns a string representation of the Workplace object.

        Returns:
            str: A string representation of the Workplace object.
        """
        return f'Workplace(name = {self.name.name},' \
             + f' capacity = {self.capacity},' \
             + f' requirements = {[str(r) for r in self.requirements]},' \
             + f' assignment = {[str(self.assignment)]})'


    def copy(self):
        """
        Creates a copy of the Workplace object.

        Returns:
            Workplace: A copy of the Workplace object.
        """
        return Workplace(
            name = self.name,
            capacity = self.capacity,
            requirements = [r.copy() for r in self.requirements],
            assignment = self.assignment.copy()
        )

# TODO: Continuar con metodos
    def assign(
        self,
        employee: Employee,
        workday: Workday
    ):
        """
        Assigns an employee to a workday in the workplace.

        Args:
            employee (Employee): The employee to be assigned.
            workday (Workday): The workday to which the employee is assigned.
        """
        if not self.assignment.get(workday.date.date,[]):
            self.assignment[workday.date.date] = []

        self.assignment[workday.date.date].append({
            'employee': employee.name,
            'workday': workday
        })


    def removeAssignment(
        self,
        date: Date,
        employee: Employee
    ):
        """
        Removes an assignment of an employee on a specific date from the workplace.

        Args:
            date (Date): The date of the assignment to be removed.
            employee (Employee): The employee whose assignment is to be removed.
        """
        print('removeAssignment:', self.name, date.date, employee.name)
        idx = [
            i for i, a in enumerate(self.assignment[date.date])
            if a['employee'] == employee.name
        ][0]
        self.assignment[date.date].pop(idx)


    def changeAssignment(
        self,
        date: Date,
        employee: Employee,
        employee_change: Employee
    ):
        """
        Changes the assignment of an employee with another employee on a specific date in the workplace.

        Args:
            date (Date): The date of the assignment to be changed.
            employee (Employee): The employee whose assignment is to be changed.
            employee_change (Employee): The employee to whom the assignment is changed.
        """
        name_a = employee.name
        name_b = employee_change.name

        assignment_a = [
            a for a in self.assignment[date.date]
            if a['employee'] == name_a
        ]
        assignment_b = [
            a for a in self.assignment[date.date]
            if a['employee'] == name_b
        ]

        if assignment_a:
            assignment_a[0]['employee'] = name_b

        if assignment_b:
            assignment_b[0]['employee'] = name_a


    def changeTurn(
        self,
        date: Date,
        employee: Employee,
        turn: Turns
    ):
        """
        Changes the turn of an employee on a specific date in the workplace.

        Args:
            date (Date): The date of the assignment.
            employee (Employee): The employee whose turn is to be changed.
            turn (Turns): The new turn for the employee.
        """
        assignment = [
            a for a in self.assignment[date.date]
            if a['employee'] == employee.name
        ]
        if assignment:
            assignment[0]['workday'].turn = turn


    def getNonCompliance(self):
        """
        Calculates the non-compliance of the workplace based on its requirements and assignment.

        Returns:
            int: The non-compliance score of the workplace.
        """
        non_compliance = []

        for r in self.requirements:
            for d in r.dates:
                for ti in getIntervals(r.time_interval):

                    compliance = [0] + [
                        1 for a in self.assignment.get(d.date, [])
                        if intervalOverlap(
                            (ti, ti + 1),
                            a['workday'].turn.value.time_interval
                        )
                    ]

                    assigned = reduce(lambda a,b: a+b, compliance)
                    non_compliance_ = r.requirement - assigned

                    non_compliance.append(
                        non_compliance_
                        if non_compliance_ >= 0
                        else non_compliance_ * - 2
                        if non_compliance_ < 0 and assigned <= self.capacity
                        else non_compliance_ * - 5
                    )

        total_non_compliance = [0 if c < 0 else c for c in non_compliance]

        return reduce(lambda a,b: a+b , total_non_compliance)


    def getWorkplan(self):
        """
        Generates the workplan for the workplace.

        Returns:
            List[Dict]: A list of dictionaries representing the workplan of the workplace.
        """
        return [
            {
                'name': self.name.name,
                **{
                    'date': d,
                    'employee': a['employee'],
                    'assignment': "{}-{}".format(
                        a['workday'].turn.value.label,
                        self.name.value
                    )
                }
            } for d, assignment in self.assignment.items() for a in assignment
        ]


class Department:

    def __init__(
        self,
        name: str,
        planning_days: List[str],
        employees: List[Employee],
        work_places: List[Workplace]
    ):
        """
        Initializes a Department object.

        Args:
            name (str): The name of the department.
            planning_days (List[str]): The planning days of the department.
            employees (List[Employee]): The employees in the department.
            work_places (List[Workplace]): The workplaces in the department.
        """
        self.name = name
        self.planning_days = planning_days
        self.employees = employees
        self.work_places = work_places


    def __str__(self):
        """
        Returns a string representation of the Department object.

        Returns:
            str: A string representation of the Department object.
        """
        return f'Department(name = {self.name}, planning_days = {self.planning_days}, employees = {[str(e) for e in self.employees]}, work_places = {[str(w) for w in self.work_places]})'


    def copy(self):
        """
        Creates a copy of the Department object.

        Returns:
            Department: A copy of the Department object.
        """
        return Department(
            name = self.name,
            planning_days = self.planning_days.copy(),
            employees = [e.copy() for e in self.employees],
            work_places = [w.copy() for w in self.work_places]
        )


    def getMetrics(
        self,
        employees_metrics: List,
        work_places_metrics: List
    ):
        """
        Calculates the metrics of the department based on employee and workplace metrics.

        Args:
            employees_metrics (List): A list of employee metrics functions.
            work_places_metrics (List): A list of workplace metrics functions.

        Returns:
            int: The overall metric score of the department.
        """
        metric = 0

        metric += reduce(
            lambda a,b: a+b,
            [e.getTimeOffWork() for e in self.employees]
        )

        metric += reduce(
            lambda a,b: a+b,
            [w.getNonCompliance() for w in self.work_places]
        )

        metric += reduce(
            lambda a,b: a+b,
            [func(e) for func in employees_metrics for e in self.employees]
        )

        metric += reduce(
            lambda a,b: a+b,
            [func(w) for func in work_places_metrics for w in self.work_places]
        )

        return metric        


    def getWorkplan(self):
        """
        Generates the workplan for the department and saves it to Excel files.
        """
        index = str(time())[:10]

        path = f'src/main/resources/{index}_employees.xlsx'
        df = pd.concat(
            [pd.DataFrame(e.getWorkplan()) for e in self.employees],
            ignore_index=True
        )
        df = df.pivot(index='name', columns='date')['assignment'].reset_index()
        df.to_excel(path, index=False)

        path = f'src/main/resources/{index}_workplaces.xlsx'
        df = pd.concat(
            [pd.DataFrame(w.getWorkplan()) for w in self.work_places],
            ignore_index=True
        )
        df = df.pivot(index=['name','employee'], columns='date')['assignment'].reset_index()
        df.to_excel(path, index=False)
