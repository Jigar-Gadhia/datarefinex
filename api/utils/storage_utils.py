from huggingface_hub import HfApi
from dotenv import load_dotenv
import os

load_dotenv()


def upload_to_hf(local_path: str):
    token = os.getenv("token")
    if not token:
        raise ValueError("Hugging Face token not set in .env (HF_TOKEN)")

    api = HfApi(token=token)
    repo = os.getenv("hf_repo")
    path_in_repo = f"cleaned/{local_path}"
    api.upload_file(
        path_or_fileobj=local_path,
        path_in_repo=path_in_repo,
        repo_id=repo,
        repo_type="dataset",
    )
    return f"https://huggingface.co/datasets/{repo}/blob/main/{path_in_repo}"
