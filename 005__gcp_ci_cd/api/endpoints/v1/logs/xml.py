from fastapi import APIRouter, HTTPException, Response
from typing import List, Dict, Any


# Crea un enrutador para agrupar los endpoints
router = APIRouter()

# Base de datos simulada (reemplaza con tu fuente de datos real)
logs_db: List[str] = [
    "<log><id>1</id><message>Log message 1</message></log>",
    "<log><id>2</id><message>Log message 2</message></log>"
]


# Define el endpoint para obtener todos los logs en formato XML
@router.get("/", response_class=Response)
def get_logs():
    """Obtiene todos los logs en formato XML."""
    return Response(content=''.join(logs_db), media_type="application/xml")


# Define el endpoint para crear un nuevo log en formato XML
@router.post("/", response_class=Response)
def create_log(log: str):
    """Crea un nuevo log en formato XML."""
    log_id = len(logs_db) + 1
    new_log = f"<log><id>{log_id}</id><message>{log}</message></log>"
    logs_db.append(new_log)
    return Response(content=new_log, media_type="application/xml")


# Define el endpoint para obtener un log específico por su ID en formato XML
@router.get("/{log_id}", response_class=Response)
def get_log(log_id: int):
    """Obtiene un log específico por su ID en formato XML."""
    log = None
    for log_entry in logs_db:
        if f"<id>{log_id}</id>" in log_entry:
            log = log_entry
            break
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return Response(content=log, media_type="application/xml")


# Define el endpoint para eliminar un log específico por su ID en formato XML
@router.delete("/{log_id}", response_class=Response)
def delete_log(log_id: int):
    """Elimina un log específico por su ID en formato XML."""
    log = None
    for log_entry in logs_db:
        if f"<id>{log_id}</id>" in log_entry:
            log = log_entry
            logs_db.remove(log_entry)
            break
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return Response(content=log, media_type="application/xml")
