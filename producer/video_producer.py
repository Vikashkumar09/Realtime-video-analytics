import cv2
import json
import time
import uuid
from kafka import KafkaProducer
from ultralytics import YOLO
import numpy as np

# =========================
# CONFIG
# =========================
KAFKA_TOPIC = "video-analytics"
BOOTSTRAP_SERVERS = "localhost:9092"   # use kafka:9092 if running inside Docker
VIDEO_SOURCE = 0  # webcam or RTSP URL
MODEL_PATH = "yolov8n.pt"
CONF_THRESHOLD = 0.5

# =========================
# INIT KAFKA PRODUCER
# =========================
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# =========================
# LOAD YOLO MODEL
# =========================
model = YOLO(MODEL_PATH)

# =========================
# VIDEO CAPTURE
# =========================
cap = cv2.VideoCapture(VIDEO_SOURCE)
assert cap.isOpened(), "❌ Cannot open video source"

print("🚀 YOLOv8 Video Producer started...")

frame_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1
    start_time = time.time()

    # =========================
    # YOLO INFERENCE
    # =========================
    results = model(frame, conf=CONF_THRESHOLD, device="cpu", verbose=False)

    latency_ms = (time.time() - start_time) * 1000

    detections = []

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label != "person":
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            detections.append({
                "label": label,
                "confidence": round(conf, 3),
                "bbox": [x1, y1, x2, y2]
            })

            # draw (for debug)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # =========================
    # MESSAGE PAYLOAD
    # =========================
    message = {
        "event_id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "frame_id": frame_id,
        "latency_ms": round(latency_ms, 2),
        "num_persons": len(detections),
        "detections": detections
    }

    # =========================
    # SEND TO KAFKA
    # =========================
    producer.send(KAFKA_TOPIC, message)

    # =========================
    # DISPLAY (OPTIONAL)
    # =========================
    cv2.putText(
        frame,
        f"Persons: {len(detections)} | Latency: {latency_ms:.1f} ms",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("YOLOv8 Producer", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
producer.flush()
producer.close()