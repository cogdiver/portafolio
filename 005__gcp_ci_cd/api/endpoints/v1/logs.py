from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from config import PROJECT_ID, TOPIC_NAME
import services.pub_sub as ps
import services.bigquery as bq


# Create a router to group the endpoints
router = APIRouter()


@router.get("/", response_model=List[dict])
def get_logs():
    """
    Get all logs.
    """
    return bq.get_logs()


@router.post("/", response_model=dict)
def create_log(log: str):
    """
    Create a new log.
    """
    message_id = ps.publish_message(PROJECT_ID, TOPIC_NAME, log)

    return {
        "id": message_id,
        "message": log
    }


@router.get("/{log_id}", response_model=dict)
def get_log(log_id: str):
    """
    Get a specific log by its ID.
    """
    logs = bq.get_log_by_id(log_id)
    if not logs:
        raise HTTPException(status_code=404, message="Log not found")
    return logs[0]


@router.delete("/{log_id}", response_model=dict)
def delete_log(log_id: str):
    """
    Delete a specific log by its ID.
    """
    logs = bq.get_log_by_id(log_id)
    if not logs:
        raise HTTPException(status_code=404, message="Log not found")
    bq.delete_log(log_id)
    return logs[0]
