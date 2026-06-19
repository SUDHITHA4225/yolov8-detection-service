#!/bin/sh
set -e

mkdir -p models
MODEL_URL="https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
MODEL_PATH="models/yolov8n.pt"

if [ -f "$MODEL_PATH" ]; then
  echo "Model already exists at $MODEL_PATH"
  exit 0
fi

if command -v curl >/dev/null 2>&1; then
  curl -L -o "$MODEL_PATH" "$MODEL_URL"
elif command -v wget >/dev/null 2>&1; then
  wget -O "$MODEL_PATH" "$MODEL_URL"
else
  echo "Error: curl or wget is required to download the model."
  exit 1
fi

echo "Model downloaded successfully to $MODEL_PATH"
