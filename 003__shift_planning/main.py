from src.main.python.model import Program
from src.main.python.utils_schemas import Date
from src.main.python.utils import plot_evolucion
from src.main.python.metrics import employees_metrics, work_places_metrics


if __name__ == '__main__':
    program = Program(
        generations = 100,
        size = 100,
        start_day = Date('2022-08-01'),
        planning_days = 30,
        crossover_probability = 0.4,
        mutation_probability = 0.3,
        employees_metrics = employees_metrics,
        work_places_metrics = work_places_metrics
    )
    better, logs = program.run()
    plot_evolucion(logs)
