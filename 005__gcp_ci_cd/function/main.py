import json
import uuid
import requests
from google.cloud import pubsub_v1


# # Nombre del tema de Pub/Sub
# # URL del servicio de Cloud Run
# TOPIC_NAME = "<TOPIC_NAME>"
# CLOUD_RUN_URL = "<CLOUD_RUN_URL>"
# PROJECT_ID = "<PROJECT>"
TOPIC_NAME = "topic_project_005"
CLOUD_RUN_URL = "<CLOUD_RUN_URL>"
PROJECT_ID = "fine-sublime-315119"



def send_to_pubsub(pubsub_message_json):
    """
    Publishes a message to a Google Cloud Pub/Sub topic.

    Args:
        pubsub_message_json (str): The JSON message to be published.

    Returns:
        str: The message ID of the published message.
    """
    # Initialize a Pub/Sub client
    publisher = pubsub_v1.PublisherClient()

    # Create the fully qualified topic path
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)

    # Publish the message to the topic
    future = publisher.publish(topic_path, data=pubsub_message_json.encode("utf-8"))

    # Get the message ID of the published message
    message_id = future.result()

    return message_id


def send_to_cloud_run(message):
    """
    Sends a message to a Google Cloud Run service.

    Args:
        message (str): The message to be sent to the Cloud Run service.

    Returns:
        tuple: A tuple containing the response text and status code from the Cloud Run service.
    """
    # Define headers for the HTTP POST request
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    # Create a dictionary with the message
    data = {"message": message}

    # Make an HTTP POST request to the Cloud Run service
    response = requests.post(CLOUD_RUN_URL, data=json.dumps(data), headers=headers)

    # Return the response text and status code as a tuple
    return response.text, response.status_code


def trigger(request):
    """
    Receives an HTTP request with a JSON body containing a 'message' and 'type' field.
    Depending on the 'type' field, it sends the 'message' either to Google Cloud Pub/Sub
    or to a specified Cloud Run service.

    Args:
        request (flask.Request): The HTTP request object.

    Returns:
        Tuple: A tuple containing a response message and an HTTP status code.
            - If successful, the response message is returned with a 200 status code.
            - If there's an error, an error message is returned with a 400 or 500 status code.
    """
    # Parse the JSON body of the request
    request_json = request.get_json()
    
    # Check if the request contains valid JSON data
    if not request_json:
        return "The request body must be a JSON.", 400
    
    # Extract 'message' and 'type' from the request JSON
    message = request_json.get("message")
    message_type = request_json.get("type")
    
    # Check if 'message' and 'type' are present in the request JSON
    if not message or not message_type:
        return "The request body must contain 'message' and 'type'.", 400
    
    if message_type == "pubsub":
        # Generate a unique ID for the message
        message_id = str(uuid.uuid4())
        
        # Create a dictionary with the message and ID
        pubsub_message = {
            "id": message_id,
            "message": message
        }
        
        # Convert the dictionary to JSON
        pubsub_message_json = json.dumps(pubsub_message)
        
        # Send the message to Pub/Sub
        send_to_pubsub(pubsub_message_json)
        
        return f"Message sent to Pub/Sub with ID: {message_id}", 200

    elif message_type == "cloud_run":
        # Send the message to Cloud Run
        cloud_run_response, status_code = send_to_cloud_run(message)
        
        if status_code == 200:
            return f"Message sent to Cloud Run: {cloud_run_response}", 200
        else:
            return f"Error sending message to Cloud Run: {cloud_run_response}", 500

    else:
        return "The value of 'type' must be 'pubsub' or 'cloud_run'.", 400
