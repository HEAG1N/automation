#!/bin/bash
ADMIN_EMAIL="your-email@example.com"


if [ "$#" -lt 2 ]; then
    echo " Error: Missing required arguments."
    echo "Usage: ./disk_usage.sh <directory_path> <max_size_mb> [threshold_percent]"
    exit 1
fi

MONITOR_DIR="$1"
MAX_SIZE_MB="$2"
THRESHOLD=${3:-80}

if [ ! -d "$MONITOR_DIR" ]; then
    echo "Error: Directory '$MONITOR_DIR' does not exist."
    exit 1
fi

echo "▶️  Checking disk usage for '$MONITOR_DIR'..."

CURRENT_USAGE_MB=$(du -sm "$MONITOR_DIR" | cut -f1)

USAGE_PERCENT=$((CURRENT_USAGE_MB * 100 / MAX_SIZE_MB))

LOG_FILE="disk_usage.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG_MESSAGE="[$TIMESTAMP] Directory '$MONITOR_DIR' is using $CURRENT_USAGE_MB MB of $MAX_SIZE_MB MB ($USAGE_PERCENT%)."

echo "$LOG_MESSAGE"
echo "$LOG_MESSAGE" >> "$LOG_FILE"

if [ "$USAGE_PERCENT" -gt "$THRESHOLD" ]; then
    echo "⚠️  Warning: Disk usage ($USAGE_PERCENT%) has exceeded the threshold of $THRESHOLD%."
    
    EMAIL_SUBJECT="Disk Usage Alert for $MONITOR_DIR"
    EMAIL_BODY="Warning: The directory '$MONITOR_DIR' is using $USAGE_PERCENT% of its allocated space ($MAX_SIZE_MB MB).\n\nPlease investigate and take action."
    
    echo -e "$EMAIL_BODY" | mail -s "$EMAIL_SUBJECT" "$ADMIN_EMAIL"
    
    echo "   An email alert has been sent to $ADMIN_EMAIL."
else
    echo " Disk usage is within the normal range."
fi

exit 0