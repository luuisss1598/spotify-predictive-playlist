#!/bin/bash
set -e  # Optional: exits on any error

# Step 1: Export Pipenv requirements
pipenv requirements > requirements.txt

# Step 2: Build Docker images without cache
docker compose build --no-cache

# Step 3: Run Airflow initialization
docker compose up airflow-init

# Step 4: Start all services
docker compose up --abort-on-container-exit
