from google.cloud import bigquery
from config import PROJECT_ID, DATASET_NAME, TABLE_NAME

# Create a BigQuery client
client = bigquery.Client(project=PROJECT_ID)


def run_query(query):
    """
    Execute a query in BigQuery and return the results.
    """
    query_job = client.query(query)
    results = query_job.result()

    # Convert results to a list of dictionaries
    rows = [dict(row.items()) for row in results]

    return rows


def get_logs():
    """
    Get all records from the logs table in BigQuery.
    """
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET_NAME}.{TABLE_NAME}`
    """
    return run_query(query)


def get_log_by_id(log_id):
    """
    Get a specific log record by its ID.
    """
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET_NAME}.{TABLE_NAME}`
        WHERE id = {log_id}
    """
    return run_query(query)
