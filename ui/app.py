import base64
import os

import requests
import streamlit as st
from PIL import Image

st.set_page_config(page_title="YOLOv8 Object Detection", layout="centered")
st.title("YOLOv8 Object Detection")

API_URL = os.getenv("API_URL", "http://api:8000/detect")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
confidence = st.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Detect Objects"):
        with st.spinner("Detecting objects..."):
            files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"confidence_threshold": str(confidence)}

            try:
                response = requests.post(API_URL, files=files, data=data, timeout=60)
                response.raise_for_status()
            except requests.RequestException as exc:
                st.error(f"API request failed: {exc}")
            else:
                result = response.json()
                st.success("Detection complete!")
                st.subheader("Summary")
                st.json(result.get("summary", {}))

                st.subheader("Detections")
                st.json(result.get("detections", []))

                annotated_base64 = result.get("annotated_image")
                if annotated_base64:
                    try:
                        annotated_bytes = base64.b64decode(annotated_base64)
                        st.image(annotated_bytes, caption="Annotated Image", use_column_width=True)
                    except Exception:
                        st.warning("Annotated image could not be displayed.")
