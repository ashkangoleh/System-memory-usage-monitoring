#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  local=$(cat .env | grep LOCAL | cut -d '=' -f2 | tr -d '[:space:]')
fi;

if [[ "$local" == "true" ]]; then
    # If local_executioner is true, run main.py
    echo "None celery scheduler running"
    python main.py
else
    # If local_executioner is false or not set, run celery commands
    echo "celery scheduler running"
    python main.py &
    celery -A src.scheduler.tasks beat -l INFO &
    celery -A src.scheduler.tasks worker --loglevel=INFO --concurrency=2
fi
