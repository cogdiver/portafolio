from src.main.python.bases import Date, Workday, Turns

from matplotlib.offsetbox import AnchoredText
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from typing import Tuple
from time import time
import random
import re


def getWorkTime(start, end):
    if start > end:
        return 24 - start + end

    return end - start


def getIntervals(time_interval: Tuple[int,int]):
    start, end = time_interval

    if start > end:
        return list(range(start, 24)) + list(range(end))
    else:
        return list(range(*time_interval))


def intervalOverlap(
    interval_a: Tuple[int,int],
    interval_b: Tuple[int,int]
):
    a = set(getIntervals(interval_a))
    b = set(getIntervals(interval_b))

    return not not a.intersection(b)


def getTimeInterval(time_interval: str):
    regex = '^\d{,2},\d{,2}$'
    ti = time_interval.replace(' ','')

    if not re.compile(regex).match(ti):
        raise Exception(
            f'Invalid time interval {time_interval}. Use the format: dd,dd'
        )

    x = [int(n) for n in ti.split(',')]

    if not all([i <= 24 for i in x]):
        raise Exception(
            f"Invalid time interval {ti}. Do not use numbers greater than 24"
        )

    return (x[0], x[1])


def getPlanningDays(start: Date, planning_days: int):
    date_format = '%Y-%m-%d'
    days = []
    x = datetime.strptime(start.date, date_format)

    for i in range(planning_days):
        y = x + timedelta(days=i)
        z = y.strftime(date_format)
        days.append(z)

    return days


def getDates(dates_interval: str):
    regex = '^20\d{2}-(:?0[1-9]|1[0-2])-\d{2}(,20\d{2}-(:?0[1-9]|1[0-2])-\d{2})*$'
    di = dates_interval.replace(' ','')

    if not re.compile(regex).match(di):
        raise Exception(
            f'Invalid dates interval format {dates_interval}. Use the format: yyyy-mm-dd for one day or yyyy-mm-dd,yyyy-mm-dd for multiple days'
        )

    x = di.split(',')

    return [Date(d) for d in x]


def crossoverDepartments(department_1, department_2, probability: float):
    department_a = department_1.copy()
    department_b = department_2.copy()

    for i in range(len(department_a.employees)):
        if random.random() <= probability:
            dates = department_a.planning_days
            date = random.choice(dates)

            empoyee_a = department_a.employees[i]
            empoyee_b = department_b.employees[i]

            workplan_a = empoyee_a.workplan[date].copy()
            workplan_b = empoyee_b.workplan[date].copy()

            workplace_name_a = workplan_a['workplace'].name
            workplace_name_b = workplan_b['workplace'].name

            workplace_a = [
                w for w in department_a.work_places
                if w.name.name == workplace_name_a
            ][0]
            workplace_b = [
                w for w in department_a.work_places
                if w.name.name == workplace_name_b
            ][0]

            # print(date)
            # print(workplace_name_a, workplace_name_b)
            # print(empoyee_a, empoyee_b)
            # print(workplace_a.assignments[date], workplace_b.assignments[date])

            empoyee_a.workplan[date] = workplan_b
            workplace_a.removeAssignment(
                date = Date(date),
                employee = empoyee_a
            )
            workplace_b.assign(
                employee = empoyee_a,
                workday = Workday(
                    turn = workplan_b['turn'],
                    date = Date(date)
                )
            )

    return department_a


def mutateDepartment(department, probability: float):
    department_ = department.copy()

    for date in department_.planning_days:
        if random.random() <= probability:
            employee_a = random.choice(department_.employees)
            name_a = employee_a.name
            workplan_a = employee_a.workplan[date].copy()
            workplace_name_a = workplan_a['workplace'].name
            workplace_a = [w for w in department_.work_places if w.name.name == workplace_name_a][0]

            employee_b = random.choice(department_.employees)
            name_b = employee_b.name
            workplan_b = employee_b.workplan[date].copy()
            workplace_name_b = workplan_b['workplace'].name
            workplace_b = [w for w in department_.work_places if w.name.name == workplace_name_b][0]

            employee_a.workplan[date] = workplan_b
            employee_b.workplan[date] = workplan_a

            workplace_a.changeAssignment(Date(date), employee_a, employee_b)
            workplace_b.changeAssignment(Date(date), employee_b, employee_a)

    return department_


def plot_evolucion(log):

    index = str(time())[:10]
    gen = log["gen"]
    fit_mins = log["min"]
    fit_maxs = log["max"]

    fig, ax1 = plt.subplots()
    ax1.plot(gen, fit_mins, "b")
    ax1.plot(gen, fit_maxs, "r")

    ax1.fill_between(gen, fit_mins, fit_maxs, facecolor='g', alpha = 0.2)
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness")
    ax1.legend(["Min", "Max"], loc="upper right")

    text = f'Min:  {min(fit_mins)}\nMax: {max(fit_maxs)}'
    anchored_text = AnchoredText(text, loc="upper center") #2
    ax1.add_artist(anchored_text)

    plt.grid(True)
    plt.savefig(f'src/main/resources/images/{index}_evolution.png', dpi=200, bbox_inches='tight')
