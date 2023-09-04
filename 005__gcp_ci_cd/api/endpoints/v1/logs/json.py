from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from services.pub_sub import publish_message

# Crea un enrutador para agrupar los endpoints
router = APIRouter()

# Base de datos simulada (reemplaza con tu fuente de datos real)
logs_db: List[Dict] = [
    {"id": 1, "message": "Log message 1"},
    {"id": 2, "message": "Log message 2"},
]

# Define el endpoint para obtener todos los logs en formato JSON
@router.get("/", response_model=List[dict])
def get_logs():
    """Obtiene todos los logs en formato JSON."""
    return logs_db


# Define el endpoint para crear un nuevo log en formato JSON
@router.post("/", response_model=dict)
def create_log(log: str):
    """Crea un nuevo log en formato JSON."""
    project_id = "fine-sublime-315119"
    topic_name = "topic_project_005"
    message_id = publish_message(project_id, topic_name, log)
    return {
        "id": message_id,
        "message": log
    }


# Define el endpoint para obtener un log específico por su ID en formato JSON
@router.get("/{log_id}", response_model=dict)
def get_log(log_id: int):
    """Obtiene un log específico por su ID en formato JSON."""
    log = list(filter(lambda log: log['id']==log_id, logs_db))
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log[0]

# Define el endpoint para eliminar un log específico por su ID en formato JSON
@router.delete("/{log_id}", response_model=dict)
def delete_log(log_id: int):
    """Elimina un log específico por su ID en formato JSON."""
    log = list(filter(lambda log: log['id']==log_id, logs_db))
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    logs_db.remove(log[0])
    return log[0]
