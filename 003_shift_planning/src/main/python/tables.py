
employees_table = [
    {
        'name': f'e{i}',
        'work_time': 48*4
    } for i in range(5)
]

absences_table = [
    {
        'employee_name': 'e1',
        'date': '2022-08-05',
        'time_interval': '8, 14'
    },
    {
        'employee_name': 'e1',
        'date': '2022-08-06',
        'time_interval': '8, 14'
    }
]

workplace_table = [
    {
        'name': 'enfermeria',
        'capacity': 3
    },
    {
        'name': 'urgencias',
        'capacity': 3
    }
]

requirements_table = [
    {
        'workplace_name': 'enfermeria',
        'time_interval': '8, 20',
        'dates': '2022-08-01,2022-08-02,2022-08-03,2022-08-04,2022-08-05',
        'requirement': 2
    },
    {
        'workplace_name': 'enfermeria',
        'time_interval': '20,8',
        'dates': '2022-08-01,2022-08-02,2022-08-03,2022-08-04,2022-08-05',
        'requirement': 1
    },
    {
        'workplace_name': 'urgencias',
        'time_interval': '8, 20',
        'dates': '2022-08-01,2022-08-02,2022-08-03,2022-08-04,2022-08-05',
        'requirement': 2
    },
    {
        'workplace_name': 'urgencias',
        'time_interval': '20,8',
        'dates': '2022-08-01,2022-08-02,2022-08-03,2022-08-04,2022-08-05',
        'requirement': 1
    }
]
