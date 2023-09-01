import yaml
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from fastapi.responses import PlainTextResponse

# Crea un enrutador para agrupar los endpoints
router = APIRouter()

# Base de datos simulada (reemplaza con tu fuente de datos real)
logs_db: List[Dict[str, Any]] = [
    {"id": 1, "message": "Log message 1"},
    {"id": 2, "message": "Log message 2"},
]

# Define el endpoint para obtener todos los logs en formato YAML
@router.get("/", response_class=PlainTextResponse)
def get_logs():
    """Obtiene todos los logs en formato YAML."""
    logs_yaml = yaml.dump(logs_db)
    return PlainTextResponse(content=logs_yaml, media_type="text/plain")

# Define el endpoint para crear un nuevo log en formato YAML
@router.post("/", response_class=PlainTextResponse)
def create_log(log: Dict[str, Any]):
    """Crea un nuevo log en formato YAML."""
    log_id = len(logs_db) + 1
    log["id"] = log_id
    logs_db.append(log)
    log_yaml = yaml.dump(log)
    return PlainTextResponse(content=log_yaml, media_type="text/plain")

# Define el endpoint para obtener un log específico por su ID en formato YAML
@router.get("/{log_id}", response_class=PlainTextResponse)
def get_log(log_id: int):
    """Obtiene un log específico por su ID en formato YAML."""
    log = next((l for l in logs_db if l["id"] == log_id), None)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    log_yaml = yaml.dump(log)
    return PlainTextResponse(content=log_yaml, media_type="text/plain")

# Define el endpoint para eliminar un log específico por su ID en formato YAML
@router.delete("/{log_id}", response_class=PlainTextResponse)
def delete_log(log_id: int):
    """Elimina un log específico por su ID en formato YAML."""
    log = next((l for l in logs_db if l["id"] == log_id), None)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    logs_db.remove(log)
    log_yaml = yaml.dump(log)
    return PlainTextResponse(content=log_yaml, media_type="text/plain")
