# 📊 DataRefineX v1 — Intelligent CSV Cleaning & Processing Pipeline

DataRefineX is a **production-ready CSV processing system** built using FastAPI, Celery, Redis, Streamlit, Docker, and HuggingFace Hub.  
It can clean huge CSV files, remove corrupted data, fix encoding issues, deduplicate rows, and upload cleaned data to a HuggingFace dataset automatically.

---

## 🚀 Features

### 🔹 CSV Cleaning Engine
- Auto-detect encoding using `chardet`
- Remove null bytes
- Chunked processing for large files (50k rows per batch)
- Auto-skip bad lines
- Deduplication
- Clean output saved as `cleaned_data.csv`

### 🔹 Background Processing with Celery
- Async job queue
- Runs independently from API
- Redis-backed broker & result store
- Track job status via FastAPI

### 🔹 Upload Cleaned Data to HuggingFace
- Uses HuggingFace Hub API
- Uploads cleaned CSV to dataset repository

### 🔹 Streamlit Frontend Dashboard
- Enter CSV URL
- Submit processing job
- Real-time progress bar
- See cleaned output + HuggingFace link

### 🔹 Fully Dockerized
- FastAPI API (`Dockerfile.api`)
- Celery Worker (`Dockerfile.worker`)
- Redis service
- Easy Compose orchestration

### 🔹 Pipenv for Dependency Management
- Clean reproducible Python environment

---

## 🏗 Architecture
- Streamlit UI → FastAPI → Celery Worker → Redis → HuggingFace Hub

---


---

## ⚙️ Environment Variables (`.env`)

```
broker_uri=redis://redis:6379/0
backend_uri=redis://redis:6379/0
token=YOUR_HUGGINGFACE_TOKEN
hf_repo=username/dataset-name
```

---

## 🐳 Install Docker (Required)

DataRefineX uses Docker and Docker Compose to run all services (API, Worker, Redis).  
Before running the project, install Docker Desktop:

### **🔹 Download Docker Desktop**
- **Windows / macOS:**  
  https://www.docker.com/products/docker-desktop/

- **Linux:**  
  Follow official installation docs:  
  https://docs.docker.com/engine/install/

### **🔹 After installation**
Make sure Docker is running:

```
docker --version
```
```
docker compose version
```


## 🐳 Running with Docker Compose

### 1️⃣ Start all services

```
docker compose up --build
```

---

### 2️⃣ Available services

| Service   | URL                          |
|-----------|-------------------------------|
| FastAPI   | http://localhost:8000/docs    |
| Streamlit | http://localhost:8501         |
| Redis     | Internal container only        |

---

### 3️⃣ Worker Logs

```
docker compose logs -f worker
```

## 🖥 Running Streamlit (Frontend)

```
streamlit run ui/app.py
```

---

## 🛠 Technology Stack

| Component        | Technology         |
|------------------|---------------------|
| Backend API      | FastAPI             |
| Background Jobs  | Celery              |
| Broker           | Redis               |
| Frontend UI      | Streamlit           |
| File Upload      | HuggingFace Hub     |
| Dependency Mgmt  | Pipenv              |
| Containers       | Docker + Compose    |

---

## ⭐ Future Improvements

- Add user authentication  
- Allow uploading local CSV files  
- Add job history  
- Email notifications  
- Distributed Celery workers  
- GPU processing for ML pipelines
- Github Actions support

---

## 🤝 Contributing

Pull requests are welcome.  
For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

MIT License.
