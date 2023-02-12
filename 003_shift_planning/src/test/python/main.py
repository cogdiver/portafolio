from src.main.python.bases import Workplaces, Turn, Turns, WorkspaceNeeds, Absence, Date, Workday
from src.main.python.schemas import Employee, Workplace, Department
from src.main.python.tables import employees_table, absences_table, requirements_table, workplace_table
from src.main.python.utils import getTimeInterval, getDates, getPlanningDays, crossoverDepartments, mutateDepartment, getWorkTime, getIntervals, intervalOverlap
from src.main.python.model import create_individual, fitness_function, selection, crossover, create_population, mutation, Program

import unittest

class BasesTest(unittest.TestCase):

    def test_date(self):
        date = '2022-07-01'

        self.assertEqual(Date(date).date, date)


    def test_turn(self):
        label = 'A'
        time_interval = (5,6)
        t = Turn(label, time_interval)

        self.assertEqual(t.label, label)
        self.assertEqual(t.time_interval, time_interval)


    def test_turns(self):
        self.assertEqual(Turns.corrido.value.label, 'C')
        self.assertEqual(Turns.corrido.value.time_interval, (8,20))

        self.assertEqual(Turns.mañana.value.label, 'M')
        self.assertEqual(Turns.mañana.value.time_interval, (8,14))

        self.assertEqual(Turns.tarde.value.label, 'T')
        self.assertEqual(Turns.tarde.value.time_interval, (14,20))

        self.assertEqual(Turns.noche.value.label, 'N')
        self.assertEqual(Turns.noche.value.time_interval, (20,8))
    
        self.assertEqual(Turns.libre.value.label, 'L')
        self.assertEqual(Turns.libre.value.time_interval, (8,20))


    def test_workplaces(self):
        self.assertEqual(Workplaces.enfermeria.value, 'E')
        self.assertEqual(Workplaces.urgencias.value, 'U')


    def test_workspace_needs(self):
        time_interval = (8,20)
        dates = [Date(f'2022-08-0{i}') for i in range(5)]
        requirement = 5

        w = WorkspaceNeeds(
            time_interval = time_interval,
            dates = dates,
            requirement = requirement
        )

        self.assertEqual(w.time_interval, time_interval)
        self.assertEqual(w.dates, dates)
        self.assertEqual(w.requirement, requirement)
        

    def test_workday(self):
        turn = Turns.corrido
        date = Date('2022-08-01')

        w = Workday(
            turn = turn,
            date = date
        )

        self.assertEqual(w.turn, turn)
        self.assertEqual(w.date, date)
        

    def test_absence(self):
        date = Date('2022-08-01')
        time_interval = (8,20)

        a = Absence(
            date = date,
            time_interval = time_interval
        )

        self.assertEqual(a.time_interval, time_interval)
        self.assertEqual(a.date, date)


class TablesTest(unittest.TestCase):

    def test_employees_table(self):
        keys = ['name','work_time']

        self.assertTrue(
            all(
                [
                    all([not not e.get(k,'') for k in keys])
                    for e in employees_table
                ]
            )
        )


    def test_absences_table(self):
        keys = ['employee_name','date','time_interval']

        self.assertTrue(
            all(
                [
                    all([not not e.get(k,'') for k in keys])
                    for e in absences_table
                ]
            )
        )


    def test_workplace_table(self):
        keys = ['name','capacity']

        self.assertTrue(
            all(
                [
                    all([not not e.get(k,'') for k in keys])
                    for e in workplace_table
                ]
            )
        )


    def test_requirements_table(self):
        keys = ['workplace_name','time_interval','dates','requirement']

        self.assertTrue(
            all(
                [
                    all([not not e.get(k,'') for k in keys])
                    for e in requirements_table
                ]
            )
        )


class SchemasTest(unittest.TestCase):

    def test_employee(self):
        name = 'name 1'
        work_time = 48
        absences = [
            Absence(
                date = Date('2022-08-02'),
                time_interval = (10,21)
            ),
            Absence(
                date = Date('2022-08-03'),
                time_interval = (14,20)
            ),
            Absence(
                date = Date('2022-08-04'),
                time_interval = (10,20)
            )
        ]

        e = Employee(
            name = name,
            work_time = work_time,
            absences = absences
        )

        e.schedule(
            workplace = Workplaces.enfermeria,
            workday = Workday(
                turn = Turns.corrido,
                date = Date('2022-08-01')
            )
        )
        e.schedule(
            workplace = Workplaces.enfermeria,
            workday = Workday(
                turn = Turns.mañana,
                date = Date('2022-08-02')
            )
        )
        e.schedule(
            workplace = Workplaces.urgencias,
            workday = Workday(
                turn = Turns.tarde,
                date = Date('2022-08-03')
            )
        )
        e.schedule(
            workplace = Workplaces.urgencias,
            workday = Workday(
                turn = Turns.noche,
                date = Date('2022-08-04')
            )
        )

        self.assertEqual(e.getTimeOffWork(), work_time - 24)
        self.assertEqual(e.getWorkplan(), [
            {
                'name': name,
                'date': '2022-08-01',
                'assignment': 'C-E'
            },
            {
                'name': name,
                'date': '2022-08-02',
                'assignment': 'L-E'
            },
            {
                'name': name,
                'date': '2022-08-03',
                'assignment': 'L-U'
            },
            {
                'name': name,
                'date': '2022-08-04',
                'assignment': 'N-U'
            },
        ])


    def test_workplace(self):
        name = Workplaces.enfermeria
        capacity = 4
        requirements = [
            WorkspaceNeeds(
                time_interval = (8,21),
                dates = [Date('2022-08-01')],
                requirement = 2
            ),
            WorkspaceNeeds(
                time_interval = (20, 8),
                dates = [Date('2022-08-01')],
                requirement = 1
            )
        ]

        e1 = Employee(name = 'employee 1', work_time = 48, absences = [])
        e2 = Employee(name = 'employee 2', work_time = 48, absences = [])
        e3 = Employee(name = 'employee 3', work_time = 48, absences = [])
        e4 = Employee(name = 'employee 4', work_time = 48, absences = [])
        e5 = Employee(name = 'employee 5', work_time = 48, absences = [])

        w = Workplace(
            name = name,
            capacity = capacity,
            requirements = requirements
        )

        w.assign(
            employee = e1,
            workday = Workday(turn = Turns.corrido, date = Date('2022-08-01'))
        )
        w.assign(
            employee = e2,
            workday = Workday(turn = Turns.mañana, date = Date('2022-08-01'))
        )
        w.assign(
            employee = e3,
            workday = Workday(turn = Turns.tarde, date = Date('2022-08-01'))
        )
        w.assign(
            employee = e4,
            workday = Workday(turn = Turns.corrido, date = Date('2022-08-01'))
        )
        w.assign(
            employee = e5,
            workday = Workday(turn = Turns.corrido, date = Date('2022-08-01'))
        )

        w.removeAssignment(
            date = Date('2022-08-01'),
            employee = e5
        )
        w.changeAssignment(
            date = Date('2022-08-01'),
            employee = e2,
            employee_change = e3
        )

        w.changeTurn(
            date = Date('2022-08-01'),
            employee = e4,
            turn = Turns.noche
        )

        self.assertEqual(w.getNonCompliance(), 1)
        self.assertEqual(w.getWorkplan(),[
            {
                'name': 'enfermeria',
                'date': '2022-08-01',
                'employee': 'employee 1',
                'assignment': 'C-E'
            },
            {
                'name': 'enfermeria',
                'date': '2022-08-01',
                'employee': 'employee 3',
                'assignment': 'M-E'
            },
            {
                'name': 'enfermeria',
                'date': '2022-08-01',
                'employee': 'employee 2',
                'assignment': 'T-E'
            },
            {
                'name': 'enfermeria',
                'date': '2022-08-01',
                'employee': 'employee 4',
                'assignment': 'N-E'
            },
        ])


    def test_department(self):
        requirements = [
            WorkspaceNeeds(
                time_interval = (8,21),
                dates = [Date(f'2022-08-0{i}') for i in range(1,5)],
                requirement = 1
            ),
            WorkspaceNeeds(
                time_interval = (20, 8),
                dates = [Date(f'2022-08-0{i}') for i in range(1,5)],
                requirement = 1
            )
        ]
        name = 'department'
        planning_days = [f'2022-08-0{i}' for i in range(1,5)]
        employees = [Employee(name=f'employee {i}', work_time=48, absences=[]) for i in range(7)]
        work_places = [
            Workplace(name=Workplaces.enfermeria, capacity=3, requirements=requirements),
            Workplace(name=Workplaces.urgencias, capacity=3, requirements=requirements)
        ]

        d = Department(
            name = name,
            planning_days = planning_days,
            employees = employees,
            work_places = work_places
        )

        # d.getWorkplan()


class UtilsTest(unittest.TestCase):

    def test_getWorkTime(self):
        self.assertEqual(getWorkTime(start=8, end=10), 2)
        self.assertEqual(getWorkTime(start=20, end=8), 12)


    def test_getIntervals(self):
        self.assertEqual(
            getIntervals(time_interval=(8,14)),
            [8,9,10,11,12,13]
        )
        self.assertEqual(
            getIntervals(time_interval=(22,4)),
            [22,23,0,1,2,3]
        )


    def test_intervalOverlap(self):
        self.assertEqual(
            intervalOverlap(
                interval_a=(8,20),
                interval_b=(8,14)
            ),
            True
        )
        self.assertEqual(
            intervalOverlap(
                interval_a=(8,14),
                interval_b=(14,20)
            ),
            False
        )


    def test_getTimeInterval(self):
        self.assertEqual(getTimeInterval(time_interval='7,8'), (7,8))
        self.assertEqual(getTimeInterval(time_interval=' 7, 8 '), (7,8))


    def test_getPlanningDays(self):
        self.assertEqual(
            getPlanningDays(
                start=Date('2022-08-30'),
                planning_days=4
            ),
            ['2022-08-30','2022-08-31','2022-09-01','2022-09-02']
        )


    def test_getDates(self):
        self.assertEqual(
            [d.date for d in getDates(dates_interval='2022-08-30, 2022-08-31, 2022-09-01')],
            ['2022-08-30','2022-08-31','2022-09-01']
        )


    def test_crossoverDepartments(self):
        pass


    def test_mutateDepartment(self):
        pass


class ModelsTest(unittest.TestCase):

    size = 4
    start_day = '2022-08-01'
    planning_days = 28
    crossover_probability = 0.2
    mutation_probability = 0.2

    e_metrics = [lambda x: 0]
    w_metrics = [lambda x: 0]


    def test_create_individual(self):
        create_individual(
            start_day = self.start_day,
            planning_days = self.planning_days
        )


    def test_create_population(self):
        self.assertEqual(
            len(create_population(self.size, self.start_day, self.planning_days)), self.size
        )


    def test_fitness_function(self):
        individual = create_individual(
            start_day = self.start_day,
            planning_days = self.planning_days
        )
        fitness_function(individual, self.e_metrics, self.w_metrics)


    def test_selection(self):
        population = create_population(self.size, self.start_day, self.planning_days)
        selected, _ , _ = selection(population, self.e_metrics, self.w_metrics)
        self.assertEqual(len(selected), len(population) // 2)


    # def test_crossover(self):
    #     population = create_population(self.size, self.start_day, self.planning_days)
    #     selected, _, _ = selection(population, self.e_metrics, self.w_metrics)
    #     new_population = crossover(selected, self.crossover_probability)
    #     self.assertEqual(len(new_population), len(population))


    def test_mutation(self):
        population = create_population(self.size, self.start_day, self.planning_days)
        mutation(population, self.mutation_probability, self.e_metrics, self.w_metrics)


    def test_program(self):
        p = Program(
            generations = 10,
            size = 10,
            start_day = Date('2022-08-01'),
            planning_days = 28,
            crossover_probability = 0.2,
            mutation_probability = 0.2,
            e_metrics = self.e_metrics,
            w_metrics = self.w_metrics
        )
        # better, logs = p.run()
