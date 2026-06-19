# YOLOv8 Object Detection Service

A containerized object detection application with a FastAPI backend and a Streamlit frontend. The backend loads a pre-trained YOLOv8 model, performs inference on uploaded images, saves annotated results to disk, and returns JSON detection data.

## Project Structure

- `api/` - FastAPI backend service
- `ui/` - Streamlit frontend service
- `models/` - Persisted YOLO model weights
- `output/` - Annotated inference output
- `scripts/download_model.sh` - Downloads the YOLOv8 model
- `docker-compose.yml` - Orchestrates `api` and `ui` services
- `.env.example` - Environment variable template

## Setup

1. Copy `.env.example` to `.env` and update values if needed.

```bash
cp .env.example .env
```

2. Build and start the application using Docker Compose.

```bash
docker-compose up --build -d
```

3. Verify services are running.

```bash
docker-compose ps
```

4. Open the web UI in your browser:

- Streamlit UI: `http://localhost:8501`
- API health: `http://localhost:8000/health`

## API Endpoints

### GET /health

Returns a simple health response.

Example response:

```json
{
  "status": "ok"
}
```

### POST /detect

Accepts a multipart/form-data request with an image file and an optional `confidence_threshold`.

Request fields:

- `image` - JPEG or PNG image file
- `confidence_threshold` - float between 0 and 1

Example response:

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

## Notes

- The YOLOv8 model weights are downloaded by `scripts/download_model.sh` during API build.
- Annotated images are saved to `output/last_annotated.jpg` on every successful detection.
- Do not commit `.env` or any model `.pt` files.

## Environment Variables

- `API_PORT` - port for the API service
- `UI_PORT` - port for the Streamlit UI
- `MODEL_PATH` - path to the YOLO model inside the container
- `CONFIDENCE_THRESHOLD_DEFAULT` - default detection confidence
- `API_URL` - URL used by the UI to call the API
- `OUTPUT_DIR` - directory to write annotated images

## Troubleshooting

- If the `api` service is unhealthy, check logs with:

```bash
docker-compose logs api
```

- If the model fails to download, ensure outbound network access is available from the Docker build environment.
