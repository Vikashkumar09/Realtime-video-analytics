from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "video-analytics",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print("📡 Kafka Consumer started...")

for msg in consumer:
    st.write(data)
    st.stop()
    data = msg.value
    print("📦 Message received:", data)