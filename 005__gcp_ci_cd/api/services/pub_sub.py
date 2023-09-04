from google.cloud import pubsub_v1


def publish_message(project_id, topic_id, message):
    """
    Publishes a message to a Pub/Sub topic.

    Args:
        project_id (str): The Google Cloud Project ID.
        topic_id (str): The ID of the Pub/Sub topic.
        message (str): The message content to be published.

    Returns:
        str: The ID of the published message.
    """
    # Create a Publisher client
    publisher = pubsub_v1.PublisherClient()

    # Prepare the topic path
    topic_path = publisher.topic_path(project_id, topic_id)

    # Convert the message to bytes
    message_bytes = message.encode("utf-8")

    # Publish the message
    future = publisher.publish(topic_path, data=message_bytes)

    # Get the message ID from the future
    message_id = future.result()

    return message_id
