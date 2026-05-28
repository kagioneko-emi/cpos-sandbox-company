from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
import threading
from main_controller import main as run_cycle

app = FastAPI()

# Setup templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Path to logs
LOG_DIR = "cpos"
AUDIT_LOG = os.path.join(LOG_DIR, "audit_log.jsonl")
POINTERS_LOG = os.path.join(LOG_DIR, "pointers.jsonl")

# @app.middleware("http")
# async def enforce_https(request: Request, call_next):
#     # Skip for local health checks if needed, but generally enforce
#     if request.url.scheme == "http" and not os.environ.get("DEBUG"):
#         url = request.url.replace(scheme="https")
#         return RedirectResponse(url)
#     return await call_next(request)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/logs")
async def get_logs():
    logs = []
    if os.path.exists(AUDIT_LOG):
        with open(AUDIT_LOG, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        logs.append(json.loads(line))
                    except:
                        continue
    return {"logs": logs}

@app.get("/api/pointers")
async def get_pointers():
    pointers = []
    if os.path.exists(POINTERS_LOG):
        with open(POINTERS_LOG, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        pointers.append(json.loads(line))
                    except:
                        continue
    return {"pointers": pointers}

@app.post("/api/trigger")
async def trigger_cycle(background_tasks: BackgroundTasks):
    # Run the main cycle in the background
    background_tasks.add_task(run_cycle)
    return {"status": "triggered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
