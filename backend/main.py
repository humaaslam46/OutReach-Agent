from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from .schemas import DraftRequest, DraftResponse, LogEntryIn, PLATFORMS, DAILY_TARGETS
from .drafting import draft_message
from . import storage

app = FastAPI(title="SafeX Outreach Assistant")


@app.get("/api/health")
def health():
    return {"message": "Outreach assistant is running"}


@app.get("/api/platforms")
def get_platforms():
    return {"platforms": PLATFORMS, "daily_targets": DAILY_TARGETS}


@app.post("/api/draft", response_model=DraftResponse)
def create_draft(req: DraftRequest):
    try:
        message = draft_message(req.business_name, req.industry, req.city, req.platform, req.notes)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Drafting failed: {type(e).__name__}")
    return DraftResponse(message=message, platform=req.platform)


@app.post("/api/log")
def create_log_entry(entry: LogEntryIn):
    saved = storage.add_entry(entry.model_dump())
    return saved


@app.get("/api/log")
def list_log_entries():
    return {"entries": storage.all_entries()}


@app.delete("/api/log/{entry_id}")
def remove_log_entry(entry_id: str):
    ok = storage.delete_entry(entry_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"deleted": entry_id}


@app.get("/api/progress")
def get_progress():
    return storage.daily_progress()


# Frontend — served at "/". Mounted last so it doesn't shadow the API routes above.
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")
