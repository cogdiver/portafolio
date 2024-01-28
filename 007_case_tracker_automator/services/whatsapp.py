import pyautogui as pg
import webbrowser as web
from time import sleep


def send_whatsapp_message(row):
    phone_number = row["CONTACTO_BASE"]
    message = row["MENSAJE"]
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    print(url)

    # Wait for page load
    web.open(url)
    x = input("Esperando...")

    # Wait to close page
    pg.hotkey('ctrl', 'w')
    sleep(2)
