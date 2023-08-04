from src.main.python.schemas import Employee, Workplace, Department
from src.main.python.utils_schemas import Date, Turns, Workplaces, WorkspaceNeeds, Workday, Absence
# from src.main.python.tables import employees_table, absences_table, requirements_table, workplace_table
from src.main.python.dataframes import df_employees, df_absences, df_workplace, df_requirements
from src.main.python.utils import getTimeInterval, getDates, getPlanningDays, crossoverDepartments, mutateDepartment, mutateEmployees

from typing import Callable
from typing import List
import pandas as pd
import random
from time import time


class Model:
    def __init__(
        self,
        start_day: Date,
        planning_days: int,
        employees_metrics: List[Callable[[Employee], int]],
        work_places_metrics: List[Callable[[Workplace], int]]
    ):
        """
        Initializes a Model object.

        Args:
            start_day (Date): The starting day for planning.
            planning_days (int): The number of planning days.
            employees_metrics (List[(Employee) -> int]): A list of employee metrics.
            work_places_metrics (List[(Workplace) -> int]): A list of work place metrics.
        """
        # Get the planning days based on the start day and planning days count
        self.p_days = getPlanningDays(start_day, planning_days)

        # Store the employees metrics and work places metrics
        self.e_metrics = employees_metrics
        self.w_metrics = work_places_metrics

        # Get the names of available work places and turns
        self.enum_workplaces = [w.name for w in Workplaces]
        self.enum_turns = [t.name for t in Turns]

        # Create a dictionary of employees
        self.employees = {
            e['name']: Employee(
                name = e['name'],
                work_time = int(e['work_time']),
                absences = [
                    Absence(
                        date = Date(a['date']),
                        time_interval = getTimeInterval(a['time_interval'])
                    ) for a in df_absences[df_absences['employee_name'] == e['name']].to_dict('records')
                ]
            ) for e in df_employees.to_dict('records')
        }

        # Create a dictionary of work places
        self.workplaces = {
            w: Workplace(
                name = Workplaces[w],
                capacity = int(df_workplace.loc[df_workplace['name'] == w, 'capacity'].iloc[0]),
                requirements = [
                    WorkspaceNeeds(
                        time_interval = getTimeInterval(r['time_interval']),
                        dates = getDates(r['dates']),
                        requirement = int(r['requirement'])
                    ) for r in df_requirements[df_requirements['workplace_name'] == w].to_dict('records')
                ]
            ) for w in self.enum_workplaces
        }


    def create_individual(self):
        """
        Creates an individual (instance) of the Department class based on the model.

        Returns:
            Department: An instance of the Department class.
        """
        # Create copies of employees and work places dictionaries
        employees = {n: e.copy() for n, e in self.employees.items()}
        workplaces = {n: w.copy() for n, w in self.workplaces.items()}

        # Iterate over employees
        for _, e in employees.items():

            # Iterate over planning days
            for d in self.p_days:

                # Randomly select a work place and turn
                w = random.choice(self.enum_workplaces)
                t = random.choice(self.enum_turns)

                # Try to schedule the employee at the selected work place and turn
                assigned = e.schedule(
                    workplace = Workplaces[w],
                    workday = Workday(
                        turn = Turns[t],
                        date = Date(d)
                    )
                )

                # If the employee was successfully scheduled, update the work place schedule
                # If the employee couldn't be scheduled, assign them as off at the work place
                turn = Turns[t] if assigned else Turns.off
                workplaces[w].schedule(
                    employee = e,
                    workday = Workday(
                        turn = turn,
                        date = Date(d)
                    )
                )

        # Create a Department instance with the generated schedule
        department = Department(
            name = f'deparment_{random.randint(100,999)}',
            planning_days = self.p_days,
            employees = employees,
            work_places = workplaces
        )

        return department


    def create_population(self, size: int):
        """
        Creates a population of individuals (instances of the Department class) based on the model.

        Args:
            size (int): The size of the population to create.

        Returns:
            List[Department]: A list of instances of the Department class representing the population.
        """
        return [self.create_individual() for _ in range(size)]


    def fitness(self, individual: Department):
        """
        Calculates the fitness value for an individual (instance of the Department class) based on the provided metrics.

        Args:
            individual (Department): An instance of the Department class representing the individual.

        Returns:
            float: The fitness value for the individual.
        """
        return individual.getMetrics(
            employees_metrics = self.e_metrics,
            work_places_metrics = self.w_metrics
        )


    def selection(self, population: List[Department], n: int):
        """
        Selects the top n individuals from the population based on fitness values.

        Args:
            population (List[Department]): The population of individuals.
            n (int): The number of individuals to select.

        Returns:
            Tuple[List[Department], float, float]: A tuple containing the selected individuals,
                the minimum fitness value among the selected individuals, and the maximum fitness
                value among the selected individuals.
        """
        # Calculate the fitness values for each individual in the population
        fitness_values = [self.fitness(p) for p in population]

        # Sort the population based on fitness values in ascending orde
        sorted_population = sorted(zip(population, fitness_values), key=lambda x: x[1])

        # Select the top n individuals with the lowest fitness values (best fitness)
        best_individuals = [i for i, _ in sorted_population[:n]]

        # Get the minimum and maximum fitness values among the selected individuals
        min_fitness = sorted_population[0][1]
        max_fitness = sorted_population[n-1][1]

        return best_individuals, min_fitness, max_fitness


    def crossover(self, parents: List[Department], probability: float):
        """
        Performs crossover between a list of parent departments to generate offspring departments.

        Args:
            parents (List[Department]): The list of parent departments.
            probability (float): The probability of crossover.

        Returns:
            List[Department]: The list of offspring departments after crossover.
        """
        offspring = []

        for _ in range(len(parents)):
            # Select two random parents from the population and create copies
            parent_a, parent_b = [p for p in random.sample(parents, k=2)]

            # Perform crossover between the two parents
            offspring.append(
                crossoverDepartments(
                    parent_a,
                    parent_b,
                    probability
                )
            )

        return offspring


    def mutation(
        self,
        parents: List[Department],
        probability: float
    ):
        """
        Applies mutation to a list of parent departments by randomly changing the work schedules of employees.

        Args:
            parents (List[Department]): The parent departments to mutate.
            probability (float): The mutation probability for each parent department.

        Returns:
            List[Department]: The mutated offspring departments.

        """
        # Apply mutation to each parent department using the mutateDepartment function
        offspring = [mutateDepartment(p, probability) for p in parents]

        # Return the mutated offspring departments
        return offspring


    def mutation_2(
        self,
        parents: List[Department],
        probability: float
    ):
        """
        Mutates the employees of each parent department in the population using the mutateEmployees function.

        Args:
            parents (List[Department]): The parent departments to be mutated.
            probability (float): The probability of mutation for each employee.

        Returns:
            List[Department]: The mutated offspring departments.
        """
        # Apply mutation to each parent department using the mutateEmployees function
        offspring = [mutateEmployees(p, probability) for p in parents]

        # Return the mutated offspring departments
        return offspring
        


class Program:
    """
    A program that runs the genetic algorithm for work scheduling optimization.
    """

    def __init__(
        self,
        generations: int,
        size: int,
        start_day: Date,
        planning_days: int,
        crossover_probability: float,
        mutation_probability: float,
        employees_metrics: List[Callable[[Employee], int]] = [lambda x: 0],
        work_places_metrics: List[Callable[[Workplace], int]] = [lambda x: 0]
    ):
        """
        Initializes the Program class.

        Args:
            generations (int): Number of generations.
            size (int): Size of the population.
            start_day (Date): Start day of the planning.
            planning_days (int): Number of planning days.
            crossover_probability (float): Probability of crossover.
            mutation_probability (float): Probability of mutation.
            employees_metrics (List[(Employee) -> int], optional): List of employee metrics functions. Defaults to [lambda x: 0].
            work_places_metrics (List[(Workplace) -> int], optional): List of work place metrics functions. Defaults to [lambda x: 0].
        """
        self.partition = 3
        self.generations = generations
        self.size = size
        self.start_day = start_day
        self.planning_days = planning_days
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.e_metrics = employees_metrics
        self.w_metrics = work_places_metrics
        self.logs = {
            'gen': [],
            'min': [],
            'max': []
        }


    def run(self):
        """
        Runs the genetic algorithm for work scheduling optimization.

        Returns:
            Tuple[int, Dict[str, List[int]]]: A tuple containing the minimum fitness value and the log data.
        """
        # Create an instance of the Model class
        m = Model(
            start_day=self.start_day,
            planning_days=self.planning_days,
            employees_metrics=self.e_metrics,
            work_places_metrics=self.w_metrics
        )

        # Create the initial population
        init_population = m.create_population(self.size)

        for g in range(self.generations):
            init_population = [p.copy() for p in init_population]
            population = [p.copy() for p in init_population]

            # Perform crossover and mutation operations on the population
            population += m.crossover(init_population, self.crossover_probability)
            population += m.mutation(init_population, self.mutation_probability)
            population += m.mutation_2(init_population, self.mutation_probability)

            # Add random individuals
            population += m.create_population(self.size)

            # Select the best individuals for the next generation
            selected, min_, max_ = m.selection(population, self.size)
            init_population = selected.copy()

            # Store the generation and fitness data in the log
            self.logs['gen'].append(g)
            self.logs['min'].append(min_)
            self.logs['max'].append(max_)

        # Select the best individual from the final population and retrieve its work schedule
        selected, min_, max_ = m.selection(population, 1)
        selected[0].getWorkplan()

        return min_, self.logs
