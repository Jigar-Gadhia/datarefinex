from fastapi import FastAPI
from api.tasks import process_csv_job
from api.tasks import celery_app

app = FastAPI()


@app.post("/process")
async def process_csv(payload: dict):
    file_url = payload.get("file_url")
    job = process_csv_job.delay(file_url)
    return {"job_id": job.id, "status": "queued"}


@app.get("/status/{job_id}")
async def job_status(job_id: str):
    result = celery_app.AsyncResult(job_id)
    if result.ready():
        return {"status": result.status, "result": result.result}
    else:
        return {"status": result.status}
