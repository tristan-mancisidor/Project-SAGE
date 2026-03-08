"""FastAPI entry point for Project SAGE."""

from __future__ import annotations

import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models.schemas import UploadResponse, AnalyzeRequest, AnalyzeResponse, ApprovalAction

load_dotenv()

app = FastAPI(title="Project SAGE", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# In-memory store for uploaded files (demo only)
uploaded_files: dict[str, dict] = {}


@app.get("/health")
def health():
    return {"status": "ok", "project": "SAGE"}


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.pdf"
    content = await file.read()
    file_path.write_bytes(content)
    uploaded_files[file_id] = {
        "filename": file.filename,
        "path": str(file_path),
    }
    return UploadResponse(file_id=file_id, filename=file.filename)


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    from agent.sage import run_sage_loop

    result = await run_sage_loop(
        file_ids=request.file_ids,
        uploaded_files=uploaded_files,
        demo_mode=request.demo_mode,
        message=request.message,
        conversation_history=request.conversation_history,
    )
    return result


@app.post("/approve", response_model=AnalyzeResponse)
async def approve(action: ApprovalAction):
    from agent.sage import run_sage_loop

    approval_message = _build_approval_message(action)
    result = await run_sage_loop(
        file_ids=[],
        uploaded_files=uploaded_files,
        demo_mode=True,
        message=approval_message,
        conversation_history=action.conversation_history,
    )
    return result


def _build_approval_message(action: ApprovalAction) -> str:
    if action.action == "approve":
        if action.section:
            return f"I approve the {action.section} section. Please continue."
        return "I approve the full plan as presented. Please finalize."
    elif action.action == "modify":
        return f"Please modify the {action.section or 'plan'}: {action.feedback}"
    elif action.action == "redirect":
        return f"Please redirect your analysis: {action.feedback}"
    return action.feedback or ""


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
