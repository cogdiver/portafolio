import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurar los parámetros del correo
gmail_user = 'psicologia.calimionorte@arquidiocesanos.edu.co'
gmail_password = 'pkpx xoxw qvtt uovz'


def send_gmail_message(message, subject, receiver, body_type='plain', cc_users=None):

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = receiver
    msg['Subject'] = subject
    msg['CC'] = cc_users

    # Cuerpo del mensaje
    msg.attach(MIMEText(message, body_type))

    # Conectar al servidor SMTP de Gmail y enviar el correo
    try:
        # Establecer la conexión con el servidor SMTP y enviar el correo electrónico
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)

        print('Correo enviado con éxito!')
    except Exception as e:
        print('Algo salió mal...', e)


def send_gmail_reply_whatsapp_message(row):
    phone_number = row["CONTACTO_BASE"]
    receiver = row["CORREO"]
    subject = "Confirmación de Contacto por WhatsApp"
    body_type = "plain"
    cc_users = "maryen.chamorro.ladino@gmail.com"

    message = f'''Se envió el siguiente mensaje al número de whatsapp {phone_number}
    {row["MENSAJE"]}
    '''

    send_gmail_message(
        message=message,
        subject=subject,
        receiver=receiver,
        body_type=body_type,
        cc_users=cc_users,
    )
