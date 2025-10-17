#!/bin/sh

# Start the system logging daemon directly
rsyslogd
# Function to create and permission the log file
create_log_file() {
    echo "Creating log file..."
    touch /var/log/cron.log
    chmod 666 /var/log/cron.log
    echo "Log file created at /var/log/cron.log"
}

# Function to monitor the log file in the background
monitor_logs() {
    echo "=== Monitoring cron logs ==="
    tail -f /var/log/cron.log
}

# Function to start the cron daemon in the foreground
run_cron() {
    echo "=== Starting cron daemon ==="
    exec cron -f
}

# Export environment variables so they are available to cron jobs
env > /etc/environment

# Run the functions
create_log_file
monitor_logs &
run_cron