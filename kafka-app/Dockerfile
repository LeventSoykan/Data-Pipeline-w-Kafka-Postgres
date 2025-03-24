# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Create the log directory and log file
RUN mkdir -p /var/log && touch /var/log/fetch_orders.log

# Copy cron job file
COPY fetch_orders_cron /etc/cron.d/fetch_orders_cron

# Set correct permissions
RUN chmod 0644 /etc/cron.d/fetch_orders_cron && crontab /etc/cron.d/fetch_orders_cron

# Start cron and application
CMD cron && tail -f /var/log/fetch_orders.log
