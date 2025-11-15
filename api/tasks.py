from celery import Celery
from api.utils.csv_utils import process_csv_file
from dotenv import load_dotenv
import os

load_dotenv()

celery_app = Celery(
    "datarefinex", broker=os.getenv("broker_uri"), backend=os.getenv("backend_uri")
)


@celery_app.task
def process_csv_job(file_url: str):
    return process_csv_file(file_url)
