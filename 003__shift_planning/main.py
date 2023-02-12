from src.main.python.model import Program
from src.main.python.bases import Date
from src.main.python.utils import plot_evolucion
from src.main.python.metrics import e_metrics, w_metrics


if __name__ == '__main__':
    program = Program(
        generations = 200,
        size = 60,
        start_day = Date('2022-08-01'),
        planning_days = 28,
        crossover_probability = 0.4,
        mutation_probability = 0.3,
        e_metrics = e_metrics,
        w_metrics = w_metrics
    )
    better, logs = program.run()
    plot_evolucion(logs)
