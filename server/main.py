from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
import uvicorn

try:
    from server.hardware import get_system_hardware
    from server.transcriber import extract_video_id, get_complete_transcript
    from server.prompt_engine import (
        chunk_transcript_to_10s_scenes,
        generate_consistent_scene_prompts,
        detect_subject_context
    )
except ImportError:
    from hardware import get_system_hardware
    from transcriber import extract_video_id, get_complete_transcript
    from prompt_engine import (
        chunk_transcript_to_10s_scenes,
        generate_consistent_scene_prompts,
        detect_subject_context
    )

app = FastAPI(
    title="imzy affilate API",
    description="Backend for YouTube Transcript to Consistent 10-Second Scene Video Prompts (Google Flow Style)",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExtractRequest(BaseModel):
    url: str = Field(..., description="YouTube video URL or video ID")
    prefer_device: str = Field("cuda", description="'cuda' or 'cpu'")

class GenerateRequest(BaseModel):
    metadata: Dict[str, Any]
    transcript_items: List[Dict[str, Any]]
    duration: float
    scene_duration: float = 10.0
    language: str = "id"
    custom_subject: Optional[str] = None
    custom_product: Optional[str] = None
    custom_setting: Optional[str] = None
    custom_style: Optional[str] = None

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "imzy affilate"}

@app.get("/api/hardware")
def get_hardware_info():
    """Returns detected GPU (RTX 3050, CUDA, VRAM) and CPU details."""
    return get_system_hardware()

@app.post("/api/extract")
def extract_youtube(req: ExtractRequest):
    """
    Extracts YouTube video metadata and complete transcript.
    Uses official YouTube transcript API or faster-whisper GPU fallback.
    """
    video_id = extract_video_id(req.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="URL YouTube tidak valid. Pastikan link video YouTube benar.")
        
    try:
        data = get_complete_transcript(video_id, device_preference=req.prefer_device)
        return {
            "status": "success",
            "video_id": video_id,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengekstrak transkrip YouTube: {str(e)}")

@app.post("/api/generate")
def generate_prompts(req: GenerateRequest):
    """
    Splits transcript into exact 10-second scenes (covering entire video duration)
    and produces visually consistent prompts with object and character continuity.
    """
    try:
        # Step 1: Chunk into 10s scenes
        raw_scenes = chunk_transcript_to_10s_scenes(
            transcript_items=req.transcript_items,
            total_duration_sec=req.duration,
            scene_duration=req.scene_duration
        )
        
        # Step 2: Generate consistent AI video generation prompts
        processed_scenes = generate_consistent_scene_prompts(
            scenes=raw_scenes,
            video_meta=req.metadata,
            language=req.language,
            custom_subject=req.custom_subject,
            custom_product=req.custom_product,
            custom_setting=req.custom_setting,
            custom_style=req.custom_style
        )
        
        anchors = processed_scenes[0]["anchors"] if processed_scenes else {}
        
        return {
            "status": "success",
            "total_scenes": len(processed_scenes),
            "scene_duration_sec": req.scene_duration,
            "video_duration_sec": req.duration,
            "anchors": anchors,
            "scenes": processed_scenes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal membuat alur prompt scene: {str(e)}")

# Mount frontend built assets if available
dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))
if os.path.exists(dist_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(dist_dir, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(dist_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(dist_dir, "index.html"))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
