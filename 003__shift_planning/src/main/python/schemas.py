from src.main.python.utils import intervalOverlap, getWorkTime, getIntervals
from src.main.python.utils_schemas import Date, Turns, Workplaces, WorkspaceNeeds, Workday, Absence

from functools import reduce
from time import time
import pandas as pd
from typing import List, Dict
from typing import Callable


class Workplan:
    """
    Class representing a work plan.

    Attributes:
        plan (Dict[str, Dict[str, Union[str, Turn]]]): A dictionary representing the work plan assignments, where the keys are dates and the values are dictionaries containing 'workplace' and 'turn' information.
    """
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
        >>> wp.assign(Date("2023-06-26"), Workplaces.nursing, Turns.morning)
        >>> wp.assign(Date("2023-06-27"), Workplaces.emergency, Turns.afternoon)
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


    def assign(
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
        >>> wp.assign(Date("2023-06-26"), Workplaces.nursing, Turns.morning)
        >>> print(wp)
        Workplan({'2023-06-26': {'workplace': 'nursing', 'turn': 'morning'}})
        """
        self.plan[date.date] = {
            'workplace': workplace,
            'turn': turn
        }


class Employee:
    """
    Class representing an employee.

    Attributes:
        name (str): The name of the employee.
        work_time (int): The total work time of the employee.
        absences (List[Absence]): A list of absences for the employee.
        workplan (Workplan): The work plan for the employee.
    """
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
            self.workplan.assign(workday.date, workplace, workday.turn)
            return True

        else:
            self.workplan.assign(workday.date, workplace, Turns.off)
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
        work_times = [0] + [getWorkTime(start, end) for start, end in intervals]
        total_work_time = reduce(lambda a,b: a+b, work_times)

        time_off_work = self.work_time - total_work_time

        return time_off_work if time_off_work >= 0 else time_off_work * -20 # TODO: Definir multiplicador


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


class Assignment:
    """
    Class representing an assignment.

    Attributes:
        value (Dict[str, Dict[str, Turn]]): A dictionary representing the assignments, where the keys are dates and the values are dictionaries containing employee names and turns.
    """
    def __init__(self, value = {}):
        """
        Initializes an Assignment object.

        Args:
            value (dict, optional): The assignments stored in a dictionary. Defaults to an empty dictionary.
        """
        self.value = value


    def __str__(self):
        """
        Returns a string representation of the Assignment object.

        Returns:
            str: A string representation of the Assignment object.
        """
        return f'Assignment({str({d: {k: str(v) for k, v in wd.items()} for d, wd in self.value.items()})})'


    def copy(self):
        """
        Creates a copy of the Assignment object.

        Returns:
            Assignment: A copy of the Assignment object.
        """
        value = {d: {e: t for e, t in a.items()} for d, a in self.value.items()}
        return Assignment(value)


    def assign(self,
        date: Date,
        employee: Employee,
        turn: Turns
    ):
        """
        Assigns a turn to an employee on a specific date.

        Args:
            date (Date): The date of the assignment.
            employee (Employee): The employee to be assigned.
            turn (Turns): The turn to be assigned.
        """
        self.value[date.date][employee.name] = turn


class Workplace:
    """
    Class representing a workplace.

    Attributes:
        name (Workplaces): The name of the workplace.
        capacity (int): The capacity of the workplace.
        requirements (List[WorkspaceNeeds]): The requirements of the workplace.
        assignment (Assignment): The assignment made to the workplace.
    """

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
            assignment (Assignment, optional): The assignment made to the workplace. Defaults to an empty Assignment object.
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


    def schedule(
        self,
        employee: Employee,
        workday: Workday
    ):
        """
        Schedules an employee for a workday at the workplace.

        Args:
            employee (Employee): The employee to be scheduled.
            workday (Workday): The workday for the scheduling.

        Returns:
            bool: True if the scheduling is successful, False otherwise.
        """
        if not self.assignment.value.get(workday.date.date):
            self.assignment.value[workday.date.date] = {}

        # if self.assignment.value[workday.date.date].get(employee.name) == workday.turn:
        #     return False

        self.assignment.assign(workday.date, employee, workday.turn)
        return True


    def removeAssignment(
        self,
        date: Date,
        employee: Employee
    ):
        """
        Removes an assignment for an employee on a specific date.

        Args:
            date (Date): The date of the assignment to be removed.
            employee (Employee): The employee of the assignment to be removed.
        """
        try:
            del self.assignment.value[date.date][employee.name]
        except:
            pass


    def getNonCompliance(self):
        """
        Calculates the non-compliance of the workplace based on its requirements and assignments.

        Returns:
            int: The non-compliance score of the workplace.
        """
        non_compliance = []

        for r in self.requirements:
            for d in r.dates:
                for ti in getIntervals(r.time_interval):

                    compliance = [0] + [
                        1 for _, t in self.assignment.value.get(d.date, {}).items()
                        if intervalOverlap(
                            (ti, ti + 1),
                            t.value.time_interval
                        )
                    ]

                    assigned = reduce(lambda a,b: a+b, compliance)
                    non_compliance_ = r.requirement - assigned

                    non_compliance.append(
                        non_compliance_ * 1 # TODO: Definir multiplicador
                        if non_compliance_ >= 0
                        else non_compliance_ * - 5 # TODO: Definir multiplicador
                        if non_compliance_ < 0 and assigned <= self.capacity
                        else non_compliance_ * - 10 # TODO: Definir multiplicador
                    )

        total_non_compliance = [0 if c < 0 else c for c in non_compliance]

        return reduce(lambda a,b: a+b , total_non_compliance)


    def getWorkplan(self):
        """
        Generates the workplan for the workplace.

        Returns:
            List[dict]: The workplan for the workplace, including date, employee, and assignment information.
        """
        return [
            {
                'name': self.name.name,
                **{
                    'date': d,
                    'employee': e,
                    'assignment': "{}-{}".format(
                        t.value.label,
                        self.name.value
                    )
                }
            } for d, a in self.assignment.value.items() for e, t in a.items()
        ]


class Department:
    """
    Class representing a department.

    Attributes:
        name (str): The name of the department.
        planning_days (List[str]): A list of planning days for the department.
        employees (Dict[str, Employee]): A dictionary of employees, where the keys are employee names and the values are Employee objects.
        work_places (Dict[str, Workplace]): A dictionary of workplaces, where the keys are workplace names and the values are Workplace objects.
    """

    def __init__(
        self,
        name: str,
        planning_days: List[str],
        employees: Dict[str, Employee],
        work_places: Dict[str, Workplace]
    ):
        """
        Initializes a Department object.

        Args:
            name (str): The name of the department.
            planning_days (List[str]): The planning days of the department.
            employees (Dict[str, Employee]): The employees in the department.
            work_places ( Dict[str, Workplace]): The workplaces in the department.
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
        return f'Department(name = {self.name}, ' \
             + f'planning_days = {self.planning_days}, ' \
             + f'employees = dict({[f"{k}: {str(e)}" for k, e in self.employees.items()]}), ' \
             + f'work_places = dict({[f"{k}: {str(w)}" for k, w in self.work_places.items()]}))'


    def copy(self):
        """
        Creates a copy of the Department object.

        Returns:
            Department: A copy of the Department object.
        """
        return Department(
            name = self.name,
            planning_days = self.planning_days.copy(),
            employees = {k: e.copy() for k, e in self.employees.items()},
            work_places = {k: w.copy() for k, w in self.work_places.items()}
        )


    def swapWorkSchedule(
        self,
        date: Date,
        employee_1: Employee,
        employee_2: Employee
    ):
        """
        Swaps the work schedule between two employees for the specified date.

        Args:
            date (Date): The date for the work schedule swap.
            employee_1 (Employee): The first employee.
            employee_2 (Employee): The second employee.
        """
        workplace_1 = self.employees[employee_1.name].workplan.plan[date.date]
        workplace_2 = self.employees[employee_2.name].workplan.plan[date.date]

        # Swap the work schedule assignments between the employees
        self.work_places[workplace_1['workplace'].name].removeAssignment(date=date, employee=employee_1)
        self.work_places[workplace_2['workplace'].name].removeAssignment(date=date, employee=employee_2)

        # Update the workday in the employees' workplans
        assigned_1 = employee_1.schedule(workplace=workplace_2['workplace'], workday=Workday(date=date, turn=workplace_2['turn']))
        assigned_2 = employee_2.schedule(workplace=workplace_1['workplace'], workday=Workday(date=date, turn=workplace_1['turn']))

        # Schedule the employee to the workplace with the new turn
        turn_2 = workplace_2['turn'] if assigned_1 else Turns.off
        turn_1 = workplace_1['turn'] if assigned_2 else Turns.off
        self.work_places[workplace_1['workplace'].name].schedule(employee=employee_2, workday=Workday(turn=turn_1, date=date))
        self.work_places[workplace_2['workplace'].name].schedule(employee=employee_1, workday=Workday(turn=turn_2, date=date))


    def changeTurn(
        self,
        date: Date,
        employee: Employee,
        new_workplace: Workplaces,
        new_turn: Turns
    ):
        """
        Changes the turn of an employee and adjusts the necessary workplace.

        Args:
            date (Date): The date for the turn change.
            employee (Employee): The employee for whom the turn will be changed.
            new_workplace (Workplace): The new workplace for the employee.
            new_turn (Turns): The new turn to assign to the employee.
        """
        # Get the current workplace assignment of the employee
        current_workplace = self.employees[employee.name].workplan.plan[date.date]['workplace']

        # Remove the current assignment from the workplace
        self.work_places[current_workplace.name].removeAssignment(date, employee)

        # Assign the new turn to the employee's workplan
        assigned = employee.schedule(new_workplace, Workday(new_turn, date))

        # Schedule the employee to the new workplace with the new turn
        turn = new_turn if assigned else Turns.off
        self.work_places[new_workplace.name].schedule(employee, Workday(turn, date))


    def getMetrics(
        self,
        employees_metrics: List[Callable[[Employee], int]],
        work_places_metrics: List[Callable[[Workplace], int]]
    ):
        """
        Calculates the overall metric value based on various metrics for employees and work places.

        Args:
            employees_metrics (List[(Employee) -> int]): A list of metric functions for employees.
                Each metric function should take an Employee object as input and return an integer metric value.
            work_places_metrics (List[(Workplace) -> int]): A list of metric functions for work places.
                Each metric function should take a Workplace object as input and return an integer metric value.

        Returns:
            int: The overall metric value calculated based on the provided metrics for employees and work places.
        """
        metric = 0

        metric += reduce(
            lambda a,b: a+b,
            [e.getTimeOffWork() for _, e in self.employees.items()]
        )

        metric += reduce(
            lambda a,b: a+b,
            [w.getNonCompliance() for _, w in self.work_places.items()]
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


    def getWorkplan(self, index: str = ''):
        """
        Generates and exports the workplan for the department's employees and workplaces.

        Returns:
            Tuple[str, str]: A tuple containing the paths to the exported workplan files for employees and workplaces.
        """
        file_name = str(time()).replace('.','') if not index else index
        path = f'src/main/resources/results/{file_name}.xlsx'

        with pd.ExcelWriter(path) as f:
            # Generate workplan for employees
            employees_workplan = pd.concat(
                [pd.DataFrame(e.getWorkplan()) for _, e in self.employees.items()],
                ignore_index=True
            )
            employees_workplan = employees_workplan.pivot(index='name', columns='date')['assignment'].reset_index()
            employees_workplan.to_excel(f, sheet_name='employees', index=False)

            # Generate workplan for workplaces
            workplaces_workplan = pd.concat(
                [pd.DataFrame(w.getWorkplan()) for _, w in self.work_places.items()],
                ignore_index=True
            )
            workplaces_workplan = workplaces_workplan.pivot(index=['name', 'employee'], columns='date')['assignment'].reset_index()
            workplaces_workplan.to_excel(f, sheet_name='workplaces', index=False)

        return path
