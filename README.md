# thoughtful

Simple FastAPI application with `/health` and `/trigger` endpoints.

## Running with nohup

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```
2. Start the server in the background:
   ```bash
   ./run_nohup.sh
   ```
   The process ID is stored in `app.pid` and output is logged to `app.log`.
