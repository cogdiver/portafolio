from fastapi import FastAPI
from endpoints.v1.logs.json import router as endpoints_v1_logs_json
from endpoints.v1.logs.xml import router as endpoints_v1_logs_xml
from endpoints.v1.logs.yaml import router as endpoints_v1_logs_yaml

app = FastAPI()

# Monta los enrutadores de los diferentes endpoints
app.include_router(endpoints_v1_logs_json, prefix="/v1/logs/json", tags=["v1/logs/json"])
app.include_router(endpoints_v1_logs_xml, prefix="/v1/logs/xml", tags=["v1/logs/xml"])
app.include_router(endpoints_v1_logs_yaml, prefix="/v1/logs/yaml", tags=["v1/logs/yaml"])


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
