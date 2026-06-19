FROM python:3.11

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        libgl1 \
        libglib2.0-0 \
        libgomp1 \
        libsm6 \
        libxrender1 \
        libxext6 \
        libx11-6 \
        libx11-xcb1 \
        libxcb1 \
        libxcb-shm0 \
        libxcb-render0 \
        libxcb-shape0 \
        libxcb-xfixes0 \
    && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/download_model.sh /app/scripts/download_model.sh
RUN chmod +x /app/scripts/download_model.sh && /app/scripts/download_model.sh

COPY api/main.py ./

ENV MODEL_PATH=/app/models/yolov8n.pt
ENV OUTPUT_DIR=/app/output
ENV OUTPUT_IMAGE_NAME=last_annotated.jpg
ENV CONFIDENCE_THRESHOLD_DEFAULT=0.25

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
