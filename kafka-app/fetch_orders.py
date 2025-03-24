
import requests
import psycopg2
from kafka import KafkaProducer
import json
import time
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(filename='/var/log/fetch_orders.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL")
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "postgres",  # Use the service name in Docker Compose
    "port": 5432
}

# Kafka connection
KAFKA_BROKER = "kafka:9092"  # Use the service name in Docker Compose
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_orders():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        if "random_orders" in data and isinstance(data["random_orders"], list):
            return data["random_orders"]  # Returns list of lists
    return []

def check_and_store_orders():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    orders = fetch_orders()
    inserted_orders = 0

    for order in orders:
        if len(order) == 5:  # Ensure correct number of fields
            timestamp, product_id, product_name, price, store_id = order

            # Check if the product already exists in the database
            cur.execute("SELECT 1 FROM orders WHERE product_id = %s", (product_id,))
            exists = cur.fetchone()

            if not exists:
                # Publish to Kafka
                producer.send("new_orders", {
                    "timestamp": timestamp,
                    "product_id": product_id,
                    "product_name": product_name,
                    "price": price,
                    "store_id": store_id,
                })

                # Insert into PostgreSQL
                cur.execute("""
                    INSERT INTO orders (timestamp, product_id, product, price, store_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (timestamp, product_id, product_name, price, store_id))
                conn.commit()
                inserted_orders += 1
    if inserted_orders > 0:
        logging.info(f"Fetched and inserted {inserted_orders} records into PostgreSQL.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    while True:
        check_and_store_orders()
        time.sleep(60)  # Wait 1 minute
