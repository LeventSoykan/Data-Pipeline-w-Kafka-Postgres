# Data Pipeline with Kafka, PostgreSQL, and FastAPI

This project implements a data pipeline using Apache Kafka, PostgreSQL, and FastAPI. It fetches new orders from an external API at regular intervals, processes them, and stores them in PostgreSQL while also publishing them to a Kafka topic for further consumption.

## Features
- **Fetch Orders**: Periodically fetches new orders from an API.
- **Store in PostgreSQL**: Orders are stored in a relational database.
- **Kafka Integration**: Orders are published to a Kafka topic for real-time processing.
- **Dockerized Deployment**: All services are containerized using Docker and managed with `docker-compose`.
- **Cron Job Execution**: Fetch script is scheduled using `cron` inside the container.

## Architecture
```
+-----------------+        +------------+        +-------------+        +-------------+
|  Fetch Orders  |  --->  |  Kafka     |  --->  |  Consumer   |  --->  |  PostgreSQL |
| (Python cron)  |        | (Orders)   |        | (Future use)|        | (Database) |
+-----------------+        +------------+        +-------------+        +-------------+
```

## Technologies Used
- **Apache Kafka**: Message broker for event-driven architecture.
- **PostgreSQL**: Relational database to store order data.
- **FastAPI**: Lightweight web framework.
- **Docker & Docker Compose**: Containerization for easy deployment.
- **Python & Kafka-Python**: Core logic for producers and consumers.

## Setup Instructions

### Prerequisites
- Docker & Docker Compose installed on your system.

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/data-pipeline.git
cd data-pipeline
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root with the following variables:
```ini
POSTGRES_USER=youruser
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=orders_db
KAFKA_BROKER_ID=1
KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
KAFKA_LISTENERS=PLAINTEXT://:9092
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"
KAFKA_LOG_RETENTION_HOURS=168
KAFKA_LOG_SEGMENT_BYTES=20971520
KAFKA_NUM_PARTITIONS=1
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
ZOOKEEPER_JVMFLAGS="-Xms128m -Xmx128m"
```

### 3. Build and Start Services
```sh
docker-compose up -d --build
```

### 4. Verify Services
Check running containers:
```sh
docker ps
```

Check Kafka topics:
```sh
docker exec -it kafka kafka-topics.sh --list --bootstrap-server kafka:9092
```

### 5. View Logs
To check fetch orders logs:
```sh
docker logs -f orders_service
```

To check PostgreSQL database:
```sh
docker exec -it postgres psql -U youruser -d orders_db
```

### 6. Stopping the Services
```sh
docker-compose down
```

## File Structure
```
.
├── fetch_orders.py       # Fetch orders script (runs with cron)
├── init.sql              # SQL script to initialize database
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Orders service Dockerfile
├── .env                  # Environment variables
└── README.md             # Project documentation
```

## Future Improvements
- Implement more consumers to process the data.
- Enhance API integration with authentication.
- Add monitoring and logging improvements.

## License
This project is open-source and available under the MIT License.

---
Happy coding! 🚀

