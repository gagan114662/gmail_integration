#!/bin/bash
# Auto-renew Gmail push notifications
# This script runs every 6 days to keep push notifications active

LOG_FILE="/Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log"
PROJECT_DIR="/Users/gaganarora/Desktop/gagan_projects/gmail_signal"

echo "=========================================" >> "$LOG_FILE"
echo "$(date): Starting push notification renewal" >> "$LOG_FILE"
echo "=========================================" >> "$LOG_FILE"

cd "$PROJECT_DIR" || exit 1

# Activate virtual environment and run setup
source venv/bin/activate

# Run the setup command to renew push notifications
python main.py setup >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): ✅ Push notifications renewed successfully" >> "$LOG_FILE"
else
    echo "$(date): ❌ Failed to renew push notifications" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
