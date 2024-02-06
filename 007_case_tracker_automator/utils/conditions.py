from datetime import datetime
import pandas as pd

from utils.clean import is_more_than_n_days_ago
from utils.clean import is_today
from utils.clean import get_follow_up_message
from utils.clean import get_documentation_message
from utils.clean import get_html_from_df
from services.whatsapp import send_whatsapp_message
from services.gmail import send_gmail_message
from services.gmail import send_gmail_reply_whatsapp_message
from vars import DOCUMENTATION_DAY, PSICO_EMAIL


def follow_up_whatsapp_message(df, execute=False):
    _filter_1 = df["REMISIÓN EXTERNA"].str.lower() == "sí"
    _filter_2 = df["ESTADO DEL CASO"].str.lower() == "seguimiento"
    _filter_3 = df["ULTIMA_ATENCION"].apply(is_more_than_n_days_ago, args=(15,))
    _filter_4 = df["FECHA_SEGUIMIENTO"].apply(is_today)
    _filter_5 = df["FECHA_SEGUIMIENTO"] == ""
    _filters = _filter_1 & _filter_2 & _filter_3 & (_filter_4 | _filter_5)

    df_filtered = df[_filters].copy(deep=True)
    if not df_filtered.empty:
        df_filtered["MENSAJE"] = df_filtered.apply(get_follow_up_message, axis=1)

    if execute:
        df_filtered.apply(send_whatsapp_message, axis=1)
        df_filtered.apply(send_gmail_reply_whatsapp_message, axis=1)

    return df_filtered


def documentation_whatsapp_message(df, execute=False):
    if datetime.now().weekday() == DOCUMENTATION_DAY:
        _filter_1 = df["REMISIÓN EXTERNA"].str.lower() == "sí"
        _filter_2 = df["ESTADO DEL CASO"].str.lower() == "espera"
        _filter_3 = df["FECHA DE CIERRE"] != ""
        _filter_4 = df["FECHA DE DOCUMENTACION"] == ""
        _filters = _filter_1 & _filter_2 & _filter_3 & _filter_4

        df_filtered = df[_filters].copy(deep=True)
        if not df_filtered.empty:
            df_filtered["MENSAJE"] = df_filtered.apply(get_documentation_message, axis=1)

        if execute:
            df_filtered.apply(send_whatsapp_message, axis=1)
            df_filtered.apply(send_gmail_reply_whatsapp_message, axis=1)

        return df_filtered
    return pd.DataFrame()


def general_info_gmail_message(df):
    _filter = df["DETALLE"] != ""
    df_filtered = df.loc[_filter, ["NOMBRE DEL ESTUDIANTE","DETALLE"]]
    df_filtered = df_filtered.copy(deep=True).reset_index(names="FILA")
    df_filtered["FILA"] = df_filtered["FILA"].apply(lambda x: x + 2)

    message = get_html_from_df(df_filtered)
    subject = "Case Tracker Automator"
    receiver = PSICO_EMAIL
    body_type = 'html'
    cc_users = None

    send_gmail_message(
        message=message,
        subject=subject,
        receiver=receiver,
        body_type=body_type,
        cc_users=cc_users,
    )
