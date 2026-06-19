import base64
import io
import os
from collections import Counter

import torch
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image, ImageDraw, ImageFont

_original_torch_load = torch.load


def _compat_torch_load(*args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _original_torch_load(*args, **kwargs)


torch.load = _compat_torch_load

from ultralytics import YOLO

app = FastAPI(title="YOLOv8 Object Detection API")

MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/yolov8n.pt")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")
OUTPUT_IMAGE_NAME = os.getenv("OUTPUT_IMAGE_NAME", "last_annotated.jpg")
CONFIDENCE_DEFAULT = float(os.getenv("CONFIDENCE_THRESHOLD_DEFAULT", "0.25"))


def ensure_model_downloaded():
    if os.path.exists(MODEL_PATH):
        return

    script_path = "/app/scripts/download_model.sh"
    if not os.path.exists(script_path):
        raise RuntimeError(
            f"Model file not found at {MODEL_PATH} and download script {script_path} is missing."
        )

    import subprocess

    subprocess.run([script_path], check=True)


ensure_model_downloaded()

try:
    model = YOLO(MODEL_PATH)
except Exception as exc:
    raise RuntimeError(f"Failed to load YOLO model from {MODEL_PATH}: {exc}") from exc


@app.get("/health")
def health_check():
    return {"status": "ok"}


def validate_image_file(upload_file: UploadFile):
    content_type = upload_file.content_type or ""
    if content_type not in {"image/jpeg", "image/jpg", "image/png"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a JPEG or PNG image.",
        )


def draw_annotation(image: Image.Image, box: list[int], label: str, score: float):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = f"{label} {score:.2f}"
    x1, y1, x2, y2 = box
    draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

    text_width, text_height = draw.textsize(text, font=font)
    label_top = max(0, y1 - text_height - 4)
    draw.rectangle(
        [x1, label_top, x1 + text_width + 6, label_top + text_height + 4],
        fill="red",
    )
    draw.text((x1 + 3, label_top + 2), text, fill="white", font=font)


@app.post("/detect")
async def detect_objects(
    image: UploadFile = File(...), confidence_threshold: float = Form(None)
):
    validate_image_file(image)

    try:
        raw_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to parse the uploaded image.")

    threshold = CONFIDENCE_DEFAULT if confidence_threshold is None else confidence_threshold
    try:
        threshold = float(threshold)
    except ValueError:
        raise HTTPException(status_code=400, detail="confidence_threshold must be a float.")

    if threshold < 0 or threshold > 1:
        raise HTTPException(status_code=400, detail="confidence_threshold must be between 0 and 1.")

    try:
        results = model(pil_image)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Model inference failed: {exc}")

    result = results[0]
    detections = []
    summary = Counter()

    annotated_image = pil_image.copy()

    names = result.names
    for row in result.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = row
        score = float(score)
        if score < threshold:
            continue

        class_index = int(class_id)
        if isinstance(names, dict):
            label = names.get(class_index, str(class_index))
        else:
            label = names[class_index] if class_index < len(names) else str(class_index)

        box = [int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))]

        detections.append({
            "box": box,
            "label": label,
            "score": round(score, 4),
        })
        summary[label] += 1
        draw_annotation(annotated_image, box, label, score)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_IMAGE_NAME)
    annotated_image.save(output_path, format="JPEG")

    buffered = io.BytesIO()
    annotated_image.save(buffered, format="JPEG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return JSONResponse(
        content={
            "detections": detections,
            "summary": dict(summary),
            "annotated_image": encoded_image,
        }
    )
