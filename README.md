# YOLOv8 Object Detection Service

A containerized object detection application built using **FastAPI**, **Streamlit**, and **YOLOv8**. The application allows users to upload an image, performs object detection using a pre-trained YOLOv8 model, returns structured JSON results, and saves an annotated image with detected objects.

---

# Features

* Real-time object detection using YOLOv8
* FastAPI REST API for inference
* Streamlit web interface
* Docker and Docker Compose support
* Configurable confidence threshold
* Detection summary by object class
* Automatic saving of annotated images
* Health check endpoint
* Environment variable configuration

---

# Project Structure

```text
yolov8-object-detection-service/
│
├── api/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── ui/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── models/
│
├── output/
│
├── scripts/
│   └── download_model.sh
│
├── docker-compose.yml
├── .env.example
├── README.md
└── .gitignore
```

---

# Technologies Used

| Category         | Technology           |
| ---------------- | -------------------- |
| Backend          | FastAPI              |
| Frontend         | Streamlit            |
| Object Detection | YOLOv8 (Ultralytics) |
| Deep Learning    | PyTorch              |
| Image Processing | OpenCV, Pillow       |
| Language         | Python               |
| Containerization | Docker               |
| Orchestration    | Docker Compose       |

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/your-username/yolov8-object-detection-service.git

cd yolov8-object-detection-service
```

## Create the Environment File

```bash
cp .env.example .env
```

Modify the values if necessary.

## Build and Start the Application

```bash
docker-compose up --build -d
```

## Verify Running Services

```bash
docker-compose ps
```

---

# Application URLs

| Service           | URL                          |
| ----------------- | ---------------------------- |
| Streamlit UI      | http://localhost:8501        |
| FastAPI API       | http://localhost:8000        |
| API Documentation | http://localhost:8000/docs   |
| Health Check      | http://localhost:8000/health |

---

# API Endpoints

## Health Check

**GET** `/health`

Response

```json
{
    "status": "ok"
}
```

---

## Object Detection

**POST** `/detect`

### Request

Content-Type:

```
multipart/form-data
```

Parameters

| Parameter            | Type                   | Required |
| -------------------- | ---------------------- | -------- |
| image                | Image File (.jpg/.png) | Yes      |
| confidence_threshold | Float                  | No       |

### Sample Response

```json
{
    "detections": [
        {
            "box": [150, 200, 250, 400],
            "label": "person",
            "score": 0.92
        }
    ],
    "summary": {
        "person": 1
    },
    "annotated_image": "<base64-encoded-image>"
}
```

---

# Application Workflow

```text
Upload Image
      │
      ▼
Streamlit UI
      │
      ▼
FastAPI Backend
      │
      ▼
YOLOv8 Model
      │
      ▼
Object Detection
      │
      ├── JSON Response
      └── Annotated Image
              │
              ▼
output/last_annotated.jpg
```

---

# Environment Variables

| Variable                     | Description                        |
| ---------------------------- | ---------------------------------- |
| API_PORT                     | Port for the FastAPI service       |
| UI_PORT                      | Port for the Streamlit application |
| API_URL                      | API endpoint used by the UI        |
| MODEL_PATH                   | Path to the YOLO model             |
| OUTPUT_DIR                   | Directory for annotated images     |
| CONFIDENCE_THRESHOLD_DEFAULT | Default confidence threshold       |

---

# Output

For every successful detection, the application:

* Returns detection results in JSON format.
* Generates a summary of detected object classes.
* Saves the annotated image to:

```text
output/last_annotated.jpg
```

---

# Docker Commands

Build Images

```bash
docker-compose build
```

Start Services

```bash
docker-compose up -d
```

Stop Services

```bash
docker-compose down
```

View API Logs

```bash
docker-compose logs api
```

---

# Example Requests

Health Check

```bash
curl http://localhost:8000/health
```

Object Detection

```bash
curl -X POST \
-F "image=@test.jpg" \
-F "confidence_threshold=0.5" \
http://localhost:8000/detect
```

---

## Conclusion

This project demonstrates a complete end-to-end object detection system using YOLOv8, FastAPI, Streamlit, and Docker. Its modular and containerized design provides a scalable foundation for deploying real-time computer vision applications.


---


