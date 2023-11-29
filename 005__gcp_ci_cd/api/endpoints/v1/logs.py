from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from typing import List, Dict, Any
from config import PROJECT_ID, TOPIC_NAME
import services.pub_sub as ps
import services.bigquery as bq
import uuid
import json

from models.logs import LogCreate

# Create a router to group the endpoints
router = APIRouter()


@router.get("/", response_model=List[dict])
def get_logs():
    """
    Get all logs.
    """
    return bq.get_logs()


@router.post("/", response_model=dict)
def create_log(log: LogCreate):
    """
    Create a new log.
    """
    message = {
        "id": str(uuid.uuid4()),
        "message": log.message
    }
    message_id = ps.publish_message(PROJECT_ID, TOPIC_NAME, json.dumps(message))

    return {**message, "message_id": message_id}


@router.get("/{log_id}", response_model=dict)
def get_log(log_id: str):
    """
    Get a specific log by its ID.
    """
    logs = bq.get_log_by_id(log_id)
    if not logs:
        raise HTTPException(status_code=404, detail="Log not found")
    return logs[0]
