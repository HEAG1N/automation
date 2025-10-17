# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm
# Install cron
RUN apt-get update && apt-get -y install cron rsyslog

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY currency_exchange_rate.py ./

# Copy the cronjob file to the cron directory
COPY cronjob /etc/cron.d/currency-cron

# Give execution rights to the cronjob file
RUN chmod 0644 /etc/cron.d/currency-cron

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["/entrypoint.sh"]