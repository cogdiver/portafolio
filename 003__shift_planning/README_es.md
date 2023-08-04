# Programa de Optimización de Programación de Trabajo

Este proyecto es un programa de optimización de programación de trabajo que utiliza algoritmos genéticos para encontrar la asignación óptima de empleados a turnos de trabajo en un determinado período de tiempo. El objetivo es maximizar la eficiencia y la satisfacción de los empleados, teniendo en cuenta las restricciones de capacidad de los lugares de trabajo y las ausencias de los empleados.

## Tablas de Datos

El programa utiliza las siguientes tablas de datos, que deben ser configuradas en el archivo [src/main/resources/tables.xlsx](./src/main/resources/tables.xlsx) antes de ejecutar el programa:

- `employees`: Contiene información sobre los empleados, incluyendo su nombre, tiempo de trabajo en horas, para el periodo a planificar.
- `absences`: Contiene información sobre las ausencias de los empleados, incluyendo la fecha y el intervalo de tiempo.
- `workplace`: Contiene información sobre los lugares de trabajo, incluyendo su nombre, capacidad e identificador.
- `requirements`: Contiene información sobre los requisitos de los lugares de trabajo, incluyendo el intervalo de tiempo, las fechas y el requisito de personal.

Asegúrate de llenar estas tablas con los datos correspondientes antes de ejecutar el programa.

## Personalización

El programa permite la personalización al definir métricas de rendimiento para empleados y lugares de trabajo. Para hacer ajustes personalizados, sigue estos pasos:

1. Abre el archivo [src/main/python/metrics.py](./src/main/python/metrics.py).
2. Define tus propias métricas de rendimiento mediante la implementación de funciones que evalúen el rendimiento de los empleados y lugares de trabajo.
3. Agregalas s las listas `employees_metrics` y `work_places_metrics` para incluir tus funciones de métricas personalizadas.

## Requisitos

Para ejecutar este programa, se requiere tener instalado Poetry, que es una herramienta de gestión de dependencias de Python. Puedes instalar Poetry siguiendo las instrucciones en su documentación oficial: [Poetry Installation](https://python-poetry.org/docs/#installation).

## Instalación

Sigue estos pasos para configurar y ejecutar el programa:

1. Clona este repositorio en tu máquina local.
2. Navega hasta la carpeta del proyecto: `cd portafolio/003__shift_planning`
3. Instala las dependencias del proyecto usando Poetry: `poetry install`

## Uso

Para ejecutar el programa y obtener la programación óptima del trabajo, sigue estos pasos:

1. Asegúrate de que las tablas de datos en el archivo [src/main/python/resources/tablas.xlsx](./src/main/python/resources/tablas.xlsx) están configuradas correctamente.
2. Ejecuta el siguiente comando en la terminal para ejecutar el programa:

```bash
poetry run python main.py
```

Esto iniciará la ejecución del programa y generará la programación óptima del trabajo. Puedes ver los resultados en [`results/`](./src/main/resources/results/) y el avance de la convergencia del modelo en [`images/`](./src/main/resources/images/) que se encuentran en la ruta [`./src/main/resources/`](./src/main/resources/).

