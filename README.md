\# Real-Time Video Analytics Platform

Deployed a real-time computer vision analytics platform on AWS using EC2, Docker, Kafka, and Streamlit with low-latency inference and scalable streaming architecture.”


Its built using YOLOv8, Apache Kafka, Streamlit, and Docker to analyze live video streams for retail insights such as customer presence, movement heatmaps, and inference latency.

“The system follows a decoupled streaming architecture.
YOLOv8 runs as a producer pushing inference metadata into Kafka.
Consumers independently compute analytics like heatmaps and latency, which are visualized in real time using Streamlit.
Kafka allows horizontal scalability and fault tolerance.”

# Features

1. Real-time object detection using YOLOv8

2. Streaming pipeline with Apache Kafka (producer → broker → consumer)

3. Live dashboard built with Streamlit

4. Customer movement heatmap

5. Inference latency monitoring

6. Fully Dockerized Kafka & Zookeeper

7. Runs locally on Windows (PowerShell / VS Code)

# System Architecture

Video Feed (Webcam / Video)
        ↓
YOLOv8 Producer (Python)
        ↓
Kafka Topic (video-analytics)
        ↓
Analytics Consumer (Python)
        ↓
Streamlit Dashboard
   ├── Heatmap
   └── Latency Metrics

# Tech Stack

| Component        | Technology              |
| ---------------- | ----------------------- |
| Object Detection | YOLOv8 (Ultralytics)    |
| Streaming        | Apache Kafka            |
| Backend          | Python                  |
| Visualization    | Streamlit               |
| Containers       | Docker & Docker Compose |
| CV Library       | OpenCV                  |
| Messaging Client | kafka-python            |


#  Project Structure

realtime-video-analytics/
│
├── producer/
│   └── video_producer.py        # YOLOv8 video producer
│
├── consumer/
│   └── analytics_consumer.py    # Kafka consumer (latency + heatmap)
│
├── dashboard/
│   └── app.py                   # Streamlit dashboard
│
├── docker-compose.yml           # Kafka & Zookeeper setup
├── yolov8n.pt                   # YOLOv8 model
├── README.md
└── .gitignore

#  Mermaid Architecture Diagram

## 🏗️ System Architecture

```mermaid
flowchart LR
    A[Camera / Video Stream] --> B[YOLOv8 Producer]
    B -->|Detections + Metadata| C[Kafka Topic: video-analytics]
    C --> D[Analytics Consumer]
    D --> E[Heatmap Generator]
    D --> F[Latency Calculator]
    E --> G[Streamlit Dashboard]
    F --> G


📌 **What this shows clearly**
- Real-time flow
- Kafka as the backbone
- Separation of producer, consumer, dashboard
- Analytics logic is explicit (heatmap + latency)

---

## ✅ Option 2: Clean ASCII Diagram (Always renders)

Use this if you want **100% compatibility everywhere**.

```md
## 🏗️ System Architecture

Camera / Video Stream
        │
        ▼
YOLOv8 Video Producer (Python)
        │
        ▼
Kafka Broker (Topic: video-analytics)
        │
        ▼
Analytics Consumer (Python)
   ┌───────────────┴───────────────┐
   │                               │
Heatmap Generator           Latency Calculator
   │                               │
   └───────────────┬───────────────┘
                   ▼
           Streamlit Dashboard
        (Live Metrics & Visualization)




