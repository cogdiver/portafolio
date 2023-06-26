from src.main.python.bases import Workplaces, Turns, WorkspaceNeeds, Absence, Date, Workday
from src.main.python.schemas import Employee, Workplace, Department
from src.main.python.tables import employees_table, absences_table, requirements_table, workplace_table
from src.main.python.utils import getTimeInterval, getDates, getPlanningDays, crossoverDepartments, mutateDepartment

from typing import List
import pandas as pd
import random


def create_individual(
    start_day: str,
    planning_days: int
):
    enum_workplaces = [w.name for w in Workplaces]
    enum_turns = [t.name for t in Turns]

    employees = [
        Employee(
            name = e['name'],
            work_time = e['work_time'],
            absences = [
                Absence(
                    date = Date(a['date']),
                    time_interval = getTimeInterval(a['time_interval'])
                ) for a in absences_table
                if a['employee_name'] == e['name']
            ]
        ) for e in employees_table
    ]

    workplaces = {
        w: Workplace(
            name = Workplaces[w],
            capacity = [
                wt for wt in workplace_table
                if wt['name'] == w
            ][0]['capacity'],
            requirements = [
                WorkspaceNeeds(
                    time_interval = getTimeInterval(r['time_interval']),
                    dates = getDates(r['dates']),
                    requirement = r['requirement']
                ) for r in requirements_table
                if r['workplace_name'] == w
            ]
        ) for w in enum_workplaces
    }

    p_days = getPlanningDays(Date(start_day), planning_days)

    for e in employees:
        for d in p_days:
            w = random.choice(enum_workplaces)
            t = random.choice(enum_turns)

            assigned = e.schedule(
                workplace = Workplaces[w],
                workday = Workday(
                    turn = Turns[t],
                    date = Date(d)
                )
            )

            if assigned:
                workplaces[w].assign(
                    employee = e,
                    workday = Workday(
                        turn = Turns[t],
                        date = Date(d)
                    )
                )
            else:
                workplaces[w].assign(
                    employee = e,
                    workday = Workday(
                        turn = Turns.libre,
                        date = Date(d)
                    )
                )

    department = Department(
        name = f'deparment_{random.randint(100,999)}',
        planning_days = p_days,
        employees = employees,
        work_places = list(workplaces.values())
    )

    return department


def create_population(
    size: int,
    start_day: str,
    planning_days: int
):
    return [
        create_individual(
            start_day,
            planning_days
        ) for _ in range(size)
    ]


def fitness_function(
    individual: Department,
    e_metrics: List,
    w_metrics: List
):
    return individual.getMetrics(
        employees_metrics = e_metrics,
        work_places_metrics = w_metrics
    )


def selection(
    population: List[Department],
    e_metrics: List,
    w_metrics: List,
    partition: int
):
    fitness = [fitness_function(i, e_metrics, w_metrics) for i in population]
    lst = pd.Series(fitness)
    index = lst.nsmallest(len(population) // partition).index.values.tolist()

    return [population[i] for i in index], min(fitness), max(fitness)

# TODO: Intercambiar Workspace
def crossover(parents: List[Department], probability: float):
    offspring = []

    for i in range(len(parents)):
        parent_a, parent_b = [p.copy() for p in random.sample(parents, k=2)]

        offspring.append(
            crossoverDepartments(
                parent_a,
                parent_b,
                probability
            )
        )

    return parents + offspring

# TODO: Cambiar turno
def mutation(
    parents: List[Department],
    probability: float,
    e_metrics: List,
    w_metrics: List
):
    lst = pd.Series([
        fitness_function(parents[i], e_metrics, w_metrics)
        for i in range(len(parents))
    ])
    idx_max = lst.nsmallest(1).index.values.tolist()[0]

    return [
        mutateDepartment(
            parents[i],
            probability
        ) if i != idx_max else parents[i].copy()
        for i in range(len(parents))
    ]


class Program:

    def __init__(
        self,
        generations: int,
        size: int,
        start_day: Date,
        planning_days: int,
        crossover_probability: float,
        mutation_probability: float,
        e_metrics: List = [lambda x: 0],
        w_metrics: List = [lambda x: 0]
    ):
        self.partition = 3
        self.generations = generations
        self.size = (size // self.partition) * self.partition
        self.start_day = start_day
        self.planning_days = planning_days
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.e_metrics = e_metrics
        self.w_metrics = w_metrics
        self.logs = {
            'gen': [],
            'min': [],
            'max': []
        }


    def run(self):
        population = create_population(self.size, self.start_day.date, self.planning_days)

        for g in range(self.generations):
            selected, min_, max_ = selection(
                population,
                self.e_metrics,
                self.w_metrics,
                self.partition
            )
            crossed = mutation(
                selected,
                self.mutation_probability,
                self.e_metrics,
                self.w_metrics
            ) # [d.copy() for d in selected] # crossover(selected, self.crossover_probability)
            new_generation = create_population(
                self.size // self.partition,
                self.start_day.date,
                self.planning_days
            )
            new_population = selected + crossed + new_generation

            population = mutation(
                new_population,
                self.mutation_probability,
                self.e_metrics,
                self.w_metrics
            )

            self.logs['gen'].append(g)
            self.logs['min'].append(min_)
            self.logs['max'].append(max_)

        fitness = [fitness_function(i, self.e_metrics, self.w_metrics) for i in population]
        lst = pd.Series(fitness)
        idx = lst.nsmallest(1).index.values.tolist()[0]
        population[idx].getWorkplan()

        return fitness[idx], self.logs
