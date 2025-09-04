#!/usr/bin/env bash
# Run the FastAPI app using nohup for persistence
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
echo $! > app.pid
