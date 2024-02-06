import re
from datetime import datetime, timedelta
import locale
from vars import PSICO_NAME, ASSISTANCE

locale.setlocale(locale.LC_TIME, 'Spanish_Spain')


def clean_number(numbers):
    numbers_list = re.findall(r'\d', numbers)
    return ''.join(numbers_list)[:10]


def get_grade_base(grade):
    return grade.split("-")[0].strip()


def get_last_date(dates):
    if not dates:
        return ""

    dates_list = re.findall(r'\d{1,2}-\d{1,2}-\d{4}', dates)

    if dates_list:
        last_date = datetime.strptime(dates_list[-1], "%d-%m-%Y")
        return last_date.strftime("%Y-%m-%d")

    dates_list = re.findall(r'\d{4}-\d{2}-\d{2}', dates)

    if dates_list:
        return dates_list[-1]

    return ""


def is_more_than_n_days_ago(date_str, n_days):
    """
    Verifica si la fecha dada más 'n' días es mayor o igual a la fecha actual.

    :param date_str: Fecha en formato string (%Y-%m-%d)
    :param n_days: Número de días a sumar a la fecha dada
    :return: True si la fecha dada más 'n' días es mayor o igual a la fecha actual, False de lo contrario
    """
    # Verificar que la fecha no sea un str vacio
    if not isinstance(date_str, str) or not date_str:
        return False

    # Convertir el string de fecha a un objeto datetime
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Sumar 'n' días a la fecha dada
    future_date = date_obj + timedelta(days=n_days)

    # Obtener la fecha actual
    current_date = datetime.now()

    # Comparar si la fecha futura es mayor o igual a la fecha actual
    return current_date >= future_date

def is_today(date_str):
    """
    Verifica si la fecha dada es igual a la fecha actual.

    :param date_str: Fecha en formato string (%Y-%m-%d)
    :return: True si la fecha dada más 'n' días es igual a la fecha actual, False de lo contrario
    """
    # Verificar que la fecha no sea un str vacio
    if not isinstance(date_str, str) or not date_str:
        return False

    # Obtener la fecha actual
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Comparar si la fecha futura es mayor o igual a la fecha actual
    return current_date == date_str


def missing_columns(row, columns, format_str="{}"):
    missing = [c for c in columns if row[c] == ""]

    return format_str.format(", ".join(missing)) if missing else ""


def saludo_segun_hora():
    # Obtener la hora actual
    hora_actual = datetime.now().hour

    # Condicionales para determinar el saludo
    if 0 <= hora_actual < 12:
        saludo = "buenos días"
    elif 12 <= hora_actual < 18:
        saludo = "buenas tardes"
    else:
        saludo = "buenas noches"

    return saludo


def get_follow_up_message(row):
    student_name = row["NOMBRE DEL ESTUDIANTE"]
    grade = row["GRADO"]
    parentezco = row["PARENTEZCO"]

    message = f"""Hola, {saludo_segun_hora()},
    Espero que se encuentre muy bien.
    Se está comunicando con usted la psicologa {PSICO_NAME}
    del colegio de {student_name} del grado {grade}.
    Me gustaría saber como va el proceso médico de su {parentezco} de acuerdo
    a la remisión externa que se le realizó.
    """

    # Eliminar saltos de línea y espacios extra
    return ' '.join(line.strip() for line in message.split('\n') if line.strip())


def get_documentation_message(row):
    
    closing_date = row["FECHA DE CIERRE"]
    fecha_objeto = datetime.strptime(closing_date, '%Y-%m-%d')
    closing_date = fecha_objeto.strftime("%d de %B").replace(" 0", " ")

    message = f"""Hola, {saludo_segun_hora()},
    El día {closing_date} se dió por finalizado el caso
    debido a que me comentaste que ya había finalizado el proceso médico.
    Sin embargo, estoy a la espera de los documentos físicos
    que certifiquen las atenciones para poder darle el cierre adecuado.
    Quedo atenta a que los haga llegar a mi oficina.
    En caso de encontrarme al venir al colegio,
    lo puedes dejar con {ASSISTANCE} que me harán llegar los documentos.
    Muchas gracias, feliz día.
    """

    # Eliminar saltos de línea y espacios extra
    message_str = ' '.join(line.strip() for line in message.split('\n') if line.strip())
    return message_str


def get_general_info_messages(df, required_columns, important_columns):
    df_temp = df.copy(deep=True)
    df_temp["DETALLE"] = ""

    # Mensaje para columnas requeridas
    format_str = "Columnas: {} necesarias en la automatización.<br/>"
    df_temp["DETALLE"] = df_temp.apply(missing_columns, axis=1, args=(required_columns, format_str))

    # Mensaje para columnas importantes
    format_str = "Columnas: {} son importantes en el registro.<br/>"
    df_temp["DETALLE"] += df_temp.apply(missing_columns, axis=1, args=(important_columns, format_str))

    # Consistencia de datos
    # - Actualizar FECHA_SEGUIMIENTO
    _filter_1 = df_temp["ULTIMA_ATENCION"].apply(is_more_than_n_days_ago, args=(16,))
    _filter_2 = df_temp["FECHA_SEGUIMIENTO"].apply(is_more_than_n_days_ago, args=(1,))
    _filter_3 = df_temp["FECHA_SEGUIMIENTO"] == ""
    _filter_4 = df_temp["ESTADO DEL CASO"].str.lower() == "seguimiento"
    _filters = _filter_1 & _filter_2 & _filter_4
    df_temp.loc[_filters, "DETALLE"] += "Recordar actualizar SEGUIMIENTO, fecha desactualizada.<br/>"
    _filters = _filter_1 & _filter_3 & _filter_4
    df_temp.loc[_filters, "DETALLE"] += "Recordar actualizar SEGUIMIENTO, no hay fecha especificada.<br/>"

    # - Si hay activación de ruta, debe haber Remisión externa
    _filter_1 = df_temp["ACTIVACIÓN DE RUTA"].str.lower() == "sí"
    _filter_2 = df_temp["REMISIÓN EXTERNA"].str.lower() != "sí"
    _filters = _filter_1 & _filter_2
    df_temp.loc[_filters, "DETALLE"] += "Si hay activación de ruta debe haber Remisión externa.<br/>"

    # - Solo se hace seguimiento a casos con Remisión externa
    _filter_1 = df_temp["ESTADO DEL CASO"].str.lower() != "cerrado"
    _filter_2 = df_temp["REMISIÓN EXTERNA"].str.lower() != "sí"
    _filters = _filter_1 & _filter_2
    df_temp.loc[_filters, "DETALLE"] += "Solo se hace seguimiento a casos con Remisión externa.<br/>"

    # - Actualizar fechas de cierre y documentación, según estado del caso
    _filter_1 = df_temp["REMISIÓN EXTERNA"].str.lower() == "sí"
    _filter_2 = df_temp["ESTADO DEL CASO"].str.lower() != "seguimiento"
    _filter_3 = df_temp["ESTADO DEL CASO"].str.lower() == "cerrado"
    _filter_4 = df_temp["FECHA DE CIERRE"] == ""
    _filter_5 = df_temp["FECHA DE DOCUMENTACION"] == ""
    _filters = _filter_1 & _filter_2 & _filter_4
    df_temp.loc[_filters, "DETALLE"] += "Actualizar FECHA DE CIERRE si el caso no está en seguimiento.<br/>"
    _filters = _filter_1 & _filter_3 & _filter_5
    df_temp.loc[_filters, "DETALLE"] += "Actualizar FECHA DE DOCUMENTACION si el caso está cerrado.<br/>"

    # - Actualizar estado del caso si hay fecha de cierre o documentación
    _filter_1 = df_temp["ESTADO DEL CASO"].str.lower() == "seguimiento"
    _filter_2 = df_temp["ESTADO DEL CASO"].str.lower() != "cerrado"
    _filter_3 = df_temp["FECHA DE CIERRE"] != ""
    _filter_4 = df_temp["FECHA DE DOCUMENTACION"] != ""
    _filters = _filter_3 & _filter_1
    df_temp.loc[_filters, "DETALLE"] += "Si hay FECHA DE CIERRE el estado del caso no debe ser seguimiento.<br/>"
    _filters = _filter_4 & _filter_2
    df_temp.loc[_filters, "DETALLE"] += "Si hay FECHA DE DOCUMENTACION el estado del caso debe ser cerrado.<br/>"

    return df_temp


def get_html_from_df(df):
    if not df.empty:
        get_tr = lambda r: f'<tr>{r}</tr>'
        get_th = lambda v: f'<th style="border: 1px solid #979797;">{v}</th>'

        # Get html for columns
        columns = [get_th(c) for c in df.columns]
        html = get_tr(''.join(columns))

        # Get html for rows
        html += df.fillna("").map(get_th).sum(axis=1).apply(get_tr).sum()

        # Get completed html
        message = f'''
        <table style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
        {html}
        </table>
        '''
    else:
        message = "No hay casos para hacer seguimiento"

    return message
