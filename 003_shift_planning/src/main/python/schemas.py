from src.main.python.bases import Absence, Workplaces, Workday, Turns, WorkspaceNeeds, Date
from src.main.python.utils import intervalOverlap, getWorkTime, getIntervals

from functools import reduce
from time import time
import pandas as pd
from typing import List, Dict


class Employee:
    def __init__(
        self,
        name: str,
        work_time: int,
        absences: List[Absence] = []
    ):
        self.name = name
        self.work_time = work_time
        self.absences = absences
        self.workplan: Dict = {}


    def __str__(self):
        return f'Employee(name = {self.name}, work_time = {self.work_time}, absences = {[str(a) for a in self.absences]}, workplan = {self.workplan})'


    def copy(self):
        employee = Employee(
            name = self.name,
            work_time = self.work_time,
            absences = [a.copy() for a in self.absences]
        )
        employee.workplan = {**self.workplan}

        return employee


    def schedule(
        self,
        workplace: Workplaces,
        workday: Workday
    ):
        if all(
            [
                not intervalOverlap(
                    a.time_interval,
                    workday.turn.value.time_interval
                ) for a in self.absences
                if a.date.date == workday.date.date
            ]
        ):
            self.workplan[workday.date.date] = {
                'workplace': workplace,
                'turn': workday.turn
            }
            return True

        else:
            self.workplan[workday.date.date] = {
                'workplace': workplace,
                'turn': Turns.libre
            }
            return False


    def getTimeOffWork(self):
        intervals = [w['turn'].value.time_interval for _, w in self.workplan.items() if w['turn'] != Turns.libre]
        total_work_time = [getWorkTime(start, end) for start, end in intervals]
        time_off_work = self.work_time - reduce(lambda a,b: a+b, total_work_time)

        return time_off_work if time_off_work > 0 else time_off_work * -2


    def getWorkplan(self):
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
            } for date, w in self.workplan.items()
        ]


class Workplace:
    def __init__(
        self,
        name: Workplaces,
        capacity: int,
        requirements: List[WorkspaceNeeds]
    ):
        self.name = name
        self.capacity = capacity
        self.requirements = requirements
        self.assignments: Dict = {}


    def __str__(self):
        return f'Workplace(name = {self.name.name}, capacity = {self.capacity}, requirements = {[str(r) for r in self.requirements]}, assignments = {[str(a) for a in self.assignments]})'


    def copy(self):
        workplace = Workplace(
            name = Workplaces[self.name.name],
            capacity = self.capacity,
            requirements = [r.copy() for r in self.requirements]
        )
        workplace.assignments = {**self.assignments}

        return workplace


    def assign(
        self,
        employee: Employee,
        workday: Workday
    ):
        if not self.assignments.get(workday.date.date,[]):
            self.assignments[workday.date.date] = []

        self.assignments[workday.date.date].append({
            'employee': employee.name,
            'workday': workday
        })


    def removeAssignment(
        self,
        date: Date,
        employee: Employee
    ):
        print('removeAssignment:', self.name, date.date, employee.name)
        idx = [
            i for i, a in enumerate(self.assignments[date.date])
            if a['employee'] == employee.name
        ][0]
        self.assignments[date.date].pop(idx)


    def changeAssignment(
        self,
        date: Date,
        employee: Employee,
        employee_change: Employee
    ):
        name_a = employee.name
        name_b = employee_change.name

        assignment_a = [
            a for a in self.assignments[date.date]
            if a['employee'] == name_a
        ]
        assignment_b = [
            a for a in self.assignments[date.date]
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
        assignment = [
            a for a in self.assignments[date.date]
            if a['employee'] == employee.name
        ]
        if assignment:
            assignment[0]['workday'].turn = turn


    def getNonCompliance(self):
        non_compliance = []

        for r in self.requirements:
            for d in r.dates:
                for ti in getIntervals(r.time_interval):

                    compliance = [0] + [
                        1 for a in self.assignments.get(d.date, [])
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
            } for d, assignment in self.assignments.items() for a in assignment
        ]


class Department:

    def __init__(
        self,
        name: str,
        planning_days: List[str],
        employees: List[Employee],
        work_places: List[Workplace]
    ):
        self.name = name
        self.planning_days = planning_days
        self.employees = employees
        self.work_places = work_places


    def __str__(self):
        return f'Department(name = {self.name}, planning_days = {self.planning_days}, employees = {[str(e) for e in self.employees]}, work_places = {[str(w) for w in self.work_places]})'


    def copy(self):
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
