from src.main.python.utils_schemas import Date, Workday, Turns

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
    """
    Performs crossover between two departments by swapping employee turns with a certain probability.

    Args:
        department_1 (Department): The first department.
        department_2 (Department): The second department.
        probability (float): The probability of swapping employee turns.

    Returns:
        Department: The resulting department after crossover.
    """
    department_a = department_1.copy()
    department_b = department_2.copy()

    for employee_name in department_a.employees:
        # Check if the crossover should occur based on the probability
        if random.random() <= probability:
            # Randomly select a date from the planning days
            date = random.choice(department_a.planning_days)

            # Get the corresponding employees in both departments
            employee_a = department_a.employees[employee_name]
            employee_b = department_b.employees[employee_name]

            # Get the workplans of the employees for the selected date
            workplan_a = employee_a.workplan.copy().plan[date]
            workplan_b = employee_b.workplan.copy().plan[date]

            # Get the names of the workplaces for the workplans
            workplace_name_a = workplan_a['workplace']
            workplace_name_b = workplan_b['workplace']

            # Swap the turns between the employees in the workplans
            department_a.changeTurn(Date(date), employee_a, workplace_name_b, workplan_b['turn'])
            department_b.changeTurn(Date(date), employee_b, workplace_name_a, workplan_a['turn'])

    return department_a


def mutateDepartment(department, probability: float):
    """
    Performs mutation on a given department by applying random changes to employees' work schedules.

    Args:
        department (Department): The department to mutate.
        probability (float): The mutation probability for each employee on each date.

    Returns:
        Department: The mutated department.
    """
    # Make a copy of the original department
    department_ = department.copy()

    # Iterate over each date in the department's planning days
    for date in department_.planning_days:
        # Check if the mutation probability is satisfied for the current date
        if random.random() <= probability:
            # Select two random employees from the department
            employee_a, employee_b = random.sample(list(department_.employees.values()), k=2)

            # Swap the work schedules of the employees for the current date
            department_.swapWorkSchedule(Date(date), employee_a, employee_b)

    return department_


def mutateEmployees(department, probability: float):
    """
    Mutates the employees of a department by changing their work schedules based on a given probability.

    Args:
        department (Department): The department object containing employees and their work schedules.
        probability (float): The probability of mutation for each employee.

    Returns:
        Department: The mutated department object.
    """
    # Make a copy of the original department
    department_ = department.copy()

    for k, employee in department_.employees.items():
        # Iterate over each date in the department's planning days
        for date in department_.planning_days:
            # Check if the crossover should occur based on the probability
            if random.random() <= probability:
                workplace = employee.workplan.plan[date]
                current_turn = workplace['turn']

                # Select two random Turns
                turns = random.sample([t for t in Turns], k=2)
                new_turn = turns[0] if turns[0] != current_turn else turns[1]

                # Change turn for the employee in date
                department_.changeTurn(Date(date), employee, workplace['workplace'], new_turn)

    return department_


def plot_evolucion(log):
    """
    Plots the evolution of fitness values over generations based on the provided log.

    Args:
        log (dict): The log containing the generation, minimum fitness values, and maximum fitness values.
    """

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
