from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
import threading
from main_controller import CorporateCycle

app = FastAPI()

# Setup templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Path to logs
LOG_DIR = "cpos"
AUDIT_LOG = os.path.join(LOG_DIR, "audit_log.jsonl")
POINTERS_LOG = os.path.join(LOG_DIR, "pointers.jsonl")

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
    return {"logs": logs[::-1]} # Return reversed for latest first

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
    return {"pointers": pointers[::-1]}

@app.get("/api/state")
async def get_state():
    cycle = CorporateCycle()
    state = cycle.load_state()
    return {"state": state}

@app.post("/api/trigger")
async def trigger_cycle(background_tasks: BackgroundTasks):
    cycle = CorporateCycle()
    background_tasks.add_task(cycle.run_to_review)
    return {"status": "triggered"}

@app.post("/api/decide")
async def make_decision(data: dict, background_tasks: BackgroundTasks):
    decision = data.get("decision") # "APPROVE" or "REJECT"
    cycle = CorporateCycle()
    background_tasks.add_task(cycle.complete_cycle, decision)
    return {"status": "decision_received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
