#!/bin/bash

PYTHON_EXEC="/Users/derzhanson/Documents/Projects/Volt/volt_app/volt/bin/python"
MANAGE_PY="/Users/derzhanson/Documents/Projects/Volt/volt_app/manage.py"
LOG_DIR="/Users/derzhanson/Documents/Projects/Volt/volt_app/logs"

# Ensure the logs directory exists
mkdir -p "$LOG_DIR"

echo "Scraping ABC data..."
$PYTHON_EXEC $MANAGE_PY scrape_abc_news >> "$LOG_DIR/logfile_scrape.log" 2>&1

echo "Indexing to Elasticsearch..."
$PYTHON_EXEC $MANAGE_PY index_to_elasticsearch >> "$LOG_DIR/logfile_index.log" 2>&1
