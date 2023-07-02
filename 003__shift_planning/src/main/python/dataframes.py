import pandas as pd

# Ruta del archivo Excel
path = "src/main/resources/tables.xlsx"

df_employees = pd.read_excel(path, dtype=str, sheet_name="employees")
df_absences = pd.read_excel(path, dtype=str, sheet_name="absences")
df_workplace = pd.read_excel(path, dtype=str, sheet_name="workplace")
df_requirements = pd.read_excel(path, dtype=str, sheet_name="requirements")
