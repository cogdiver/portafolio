# Shift Planning Optimization Program

This project is a shift planning optimization program that utilizes genetic algorithms to find the optimal assignment of employees to work shifts within a specified time period. The goal is to maximize efficiency and employee satisfaction while considering workplace capacity constraints and employee absences.

## Data Tables

The program uses the following data tables, which need to be configured in the [src/main/python/resources/tablas.xlsx](./src/main/python/resources/tablas.xlsx) file before running the program:

- `employees`: Contains information about the employees, including their name, work time in hours for the planning period.
- `absences`: Contains information about employee absences, including the date and time interval.
- `workplace`: Contains information about the workplaces, including their name, capacity, and identifier.
- `requirements`: Contains information about the workplace requirements, including the time interval, dates, and staffing requirement.

Make sure to fill in these tables with the corresponding data before running the program.

## Customization

The program allows for customization by defining performance metrics for employees and workplaces. To make custom adjustments, follow these steps:

1. Open the [src/main/python/metrics.py](./src/main/python/metrics.py) file.
2. Define your own performance metrics by implementing functions that evaluate the performance of employees and workplaces.
3. Add the functions to `employees_metrics` and `work_places_metrics` lists to include your custom metrics functions.

## Requirements

To run this program, Poetry needs to be installed, which is a Python dependency management tool. You can install Poetry by following the instructions in their official documentation: [Poetry Installation](https://python-poetry.org/docs/#installation).

## Installation

Follow these steps to set up and run the program:

1. Clone this repository to your local machine.
2. Navigate to the project folder: `cd portafolio/003__shift_planning`
3. Install the project dependencies using Poetry: `poetry install`

## Usage

To execute the program and obtain the optimal shift planning, follow these steps:

1. Ensure that the data tables in the [src/main/python/resources/tablas.xlsx](./src/main/python/resources/tablas.xlsx) file are properly configured.
2. Run the following command in the terminal to execute the program:

```bash
poetry run python main.py
```

This will initiate the program execution and generate the optimal shift planning. You can view the results in the [`results/`](./src/main/resources/results/) directory and the convergence progress of the model in the [`images/`](./src/main/resources/images/) directory located at [`./src/main/resources/`](./src/main/resources/).

