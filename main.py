from fastapi import FastAPI
from api.tasks import process_csv_job

app = FastAPI()


@app.post("/process")
async def process_csv(payload: dict):
    file_url = payload.get("file_url")
    job = process_csv_job.delay(file_url)
    return {"job_id": job.id, "status": "queued"}


@app.get("/status/{job_id}")
async def job_status(job_id: str):
    from api.tasks import celery_app

    result = celery_app.AsyncResult(job_id)
    return {"id": job_id, "status": result.status, "result": result.result}
