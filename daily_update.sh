#!/bin/bash

# This script sets up a cron job to run the fetch_api_data.py script daily at 2 AM.

# Path to the script and logfile
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/manage.py fetch_api_data"
LOG_FILE="$SCRIPT_DIR/logfile.log"

# Add the cron job
( crontab -l 2>/dev/null; echo "0 2 * * * /usr/bin/python3 $SCRIPT_PATH >> $LOG_FILE 2>&1" ) | crontab -

current_date=$(date +"%d-%m-%Y %H:%M")

{
  echo "Automated update to fetch API hotel data at: $current_date"
} >> "$LOG_FILE"

echo "Added cronjob to fetch api data at 2 AM"
