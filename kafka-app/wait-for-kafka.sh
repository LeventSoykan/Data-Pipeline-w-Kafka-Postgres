#!/bin/sh
# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
while ! nc -z kafka 9092; do
  sleep 1
done
echo "Kafka is up!"

# Start both Python scripts
python fetch_orders.py & python consume_orders.py
