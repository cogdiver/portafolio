import sys
import pandas as pd
from utils.clean import get_last_date
from utils.clean import get_grade_base
from utils.clean import clean_number
from utils.clean import missing_columns
from utils.clean import get_general_info_messages
from utils.conditions import general_info_gmail_message
from utils.conditions import follow_up_whatsapp_message
from utils.conditions import documentation_whatsapp_message
from utils.config import path, required_columns, important_columns




def main():
    df = pd.read_excel(path, dtype=str)

    # for c in required_columns + important_columns:
    _filter = df["ACTIVO"].str.lower() == "sí"
    df = df[_filter].fillna("")

    df["CONTACTO_BASE"] = df["CONTACTO"].apply(clean_number)
    df["GRADO_BASE"] = df["GRADO"].apply(get_grade_base)
    df["ULTIMA_ATENCION"] = df["FECHA ATENCIONES"].apply(get_last_date)
    df["FECHA_SEGUIMIENTO"] = df["SEGUIMIENTO"].apply(get_last_date)
    df["FECHA DE CIERRE"] = df["FECHA DE CIERRE"].apply(get_last_date)


    df = get_general_info_messages(df, required_columns, important_columns)

    if len(sys.argv) > 1:
        execute = sys.argv[1] == "-e"

        # No considerar registros con datos imcompletos
        df_temp = df[df.apply(missing_columns, axis=1, args=(required_columns,)) == ""]

        # Envio de mensajes de seguimiento
        df_follow_up = follow_up_whatsapp_message(df_temp, execute)
        df.loc[df_follow_up.index, "DETALLE"] += "Se envía mensaje de seguimiento, recuerda actualizar próximo seguimiento o estado."

        # Envio de mensajes solicitando documentación
        df_documentation = documentation_whatsapp_message(df_temp, execute)
        df.loc[df_documentation.index, "DETALLE"] += "Se envía mensaje solicitando documentación, recuerda actualizar estado."

    general_info_gmail_message(df)
    return df


if __name__ == "__main__":
    main()
