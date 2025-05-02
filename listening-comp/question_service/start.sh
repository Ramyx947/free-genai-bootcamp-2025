#!/bin/bash

echo "Starting question service..."
exec uvicorn main:app --host 0.0.0.0 --port 8002 --log-level debug