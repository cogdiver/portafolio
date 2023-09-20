import os
import json
import base64
from google.cloud import pubsub_v1
import requests

# Nombre del tema de Pub/Sub
topic_name = "topic_project_005"

# URL del servicio de Cloud Run
cloud_run_url = "https://image-project-005-55nsgsicwq-uc.a.run.app/v1/logs/"

def trigger(request, context):
    # # Extraer el mensaje de la solicitud HTTP
    # request_json = request.get_json(silent=True)
    # if request_json and 'message' in request_json:
    #     message = request_json['message']
    # else:
    #     return 'Bad Request: El cuerpo de la solicitud debe contener un campo "message"', 400

    # # Crear un cliente de Pub/Sub
    # publisher = pubsub_v1.PublisherClient()

    # # Formatear el mensaje en bytes
    # message_bytes = message.encode('utf-8')

    # # Publicar el mensaje en Pub/Sub
    # topic_path = publisher.topic_path(os.environ['GOOGLE_CLOUD_PROJECT'], topic_name)
    # future = publisher.publish(topic_path, data=message_bytes)
    # message_id = future.result()

    # # Realizar la petición a Cloud Run
    # response = requests.post(cloud_run_url, json={"message": message})
    
    # return f'Mensaje publicado en Pub/Sub con ID: {message_id}, Respuesta de Cloud Run: {response.text}'
    print(request)
    return 'OK'
