import time
from kafka import KafkaConsumer

KAFKA_BROKER = "kafka:9092"  # Ensure this matches your Docker setup

# Wait for Kafka to be ready
while True:
    try:
        consumer = KafkaConsumer(
            "new_orders",
            bootstrap_servers=KAFKA_BROKER,
            auto_offset_reset="earliest",
            group_id="order-consumers"
        )
        print("Kafka is up!")
        break  # Exit loop if Kafka is ready
    except Exception as e:
        print(f"Waiting for Kafka to be ready... Error: {e}")
        time.sleep(5)  # Wait and retry

# Now start consuming messages
for message in consumer:
    print(f"Received: {message.value.decode()}")
