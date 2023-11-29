from fastapi import FastAPI
from endpoints.v1.logs import router as endpoints_v1_logs

app = FastAPI()

# Monta los enrutadores de los diferentes endpoints
app.include_router(endpoints_v1_logs, prefix="/v1/logs", tags=["v1/logs"])


@app.get("/")
def read_root():
    return {"message": "Welcome to GCP CI/CD project"}
