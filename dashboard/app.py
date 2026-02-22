import streamlit as st
from kafka import KafkaConsumer
import json
import numpy as np
import cv2
from collections import deque

# -------------------------------
# Streamlit setup
# -------------------------------
st.set_page_config(page_title="Real-Time Video Analytics", layout="wide")
st.title("📊 Real-Time Video Analytics Dashboard")

latency_placeholder = st.empty()
count_placeholder = st.empty()
heatmap_placeholder = st.empty()

# -------------------------------
# Kafka Consumer
# -------------------------------
consumer = KafkaConsumer(
    "video-analytics",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

# -------------------------------
# Heatmap state
# -------------------------------
HEATMAP_SIZE = (480, 640)
heatmap_accumulator = np.zeros(HEATMAP_SIZE, dtype=np.float32)

# Keep last N latencies for smoothing
latency_buffer = deque(maxlen=20)

# -------------------------------
# Stream loop
# -------------------------------
for msg in consumer:
    data = msg.value

    latency = data.get("latency_ms", 0)
    detections = data.get("detections", [])

    latency_buffer.append(latency)
    avg_latency = sum(latency_buffer) / len(latency_buffer)

    # Update metrics
    latency_placeholder.metric(
        "⏱ Avg Inference Latency (ms)",
        f"{avg_latency:.2f}"
    )

    count_placeholder.metric(
        "🧍 People Detected",
        len(detections)
    )

   # ---- Heatmap update ----
for det in data.get("detections", []):

    if "bbox" not in det:
        continue

    x1, y1, x2, y2 = det["bbox"]

    cx = int((x1 + x2) / 2)
    cy = int((y1 + y2) / 2)

    if 0 <= cy < heatmap.shape[0] and 0 <= cx < heatmap.shape[1]:
        heatmap[cy, cx] += 1

    # Normalize + colorize heatmap
    heatmap_norm = cv2.normalize(
        heatmap_accumulator, None, 0, 255, cv2.NORM_MINMAX
    ).astype(np.uint8)

    heatmap_color = cv2.applyColorMap(
        heatmap_norm, cv2.COLORMAP_JET
    )

    heatmap_placeholder.image(
        heatmap_color,
        caption="🔥 Customer Footfall Heatmap",
        channels="BGR",
        use_column_width=True
    )
