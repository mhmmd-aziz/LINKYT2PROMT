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
        detect_subject_context,
        extract_kids_video_vision
    )
    from server.gemini_service import (
        verify_gemini_key,
        analyze_uploaded_image,
        generate_kids_prompts_with_gemini
    )
except ImportError:
    from hardware import get_system_hardware
    from transcriber import extract_video_id, get_complete_transcript
    from prompt_engine import (
        chunk_transcript_to_10s_scenes,
        generate_consistent_scene_prompts,
        detect_subject_context,
        extract_kids_video_vision
    )
    from gemini_service import (
        verify_gemini_key,
        analyze_uploaded_image,
        generate_kids_prompts_with_gemini
    )

app = FastAPI(
    title="imsy tools yt API",
    description="Backend for Kids YouTube Video Remake to 60 Consistent 10s Scene Prompts (Google Flow Style)",
    version="2.0.0"
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

class AnalyzeImageRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image string (1 photo)")
    gemini_api_key: Optional[str] = Field(None, description="Optional Gemini API key")

class VerifyKeyRequest(BaseModel):
    gemini_api_key: str = Field(..., description="Gemini API Key to test")

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
    image_context: Optional[Dict[str, Any]] = None
    gemini_api_key: Optional[str] = None

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "imsy tools yt"}

@app.get("/api/hardware")
def get_hardware_info():
    """Returns detected GPU (RTX 3050, CUDA, VRAM) and CPU details."""
    return get_system_hardware()

@app.post("/api/gemini/verify")
def api_verify_gemini_key(req: VerifyKeyRequest):
    """Checks validity of user-supplied Google Gemini API key."""
    res = verify_gemini_key(req.gemini_api_key)
    return res

@app.post("/api/analyze-image")
def api_analyze_image(req: AnalyzeImageRequest):
    """
    Analyzes 1 uploaded toy car / kids character / setting image.
    Uses Gemini Vision Multimodal if API key provided, or smart local kids vision engine.
    """
    try:
        analysis = analyze_uploaded_image(req.image_base64, api_key=req.gemini_api_key)
        return {
            "status": "success",
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menganalisis gambar: {str(e)}")

@app.post("/api/extract")
def extract_youtube(req: ExtractRequest):
    """
    Extracts YouTube video metadata, complete transcript, and automatically
    understands the core video vision (tema mainan anak, balapan mobil, dsb).
    """
    video_id = extract_video_id(req.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="URL YouTube tidak valid. Pastikan link video YouTube benar.")
        
    try:
        data = get_complete_transcript(video_id, device_preference=req.prefer_device)
        
        # Analyze and extract Kids Video Vision
        title = data["metadata"].get("title", "")
        full_text = data.get("full_text", "")
        vision = extract_kids_video_vision(title, full_text)
        
        data["video_vision"] = vision
        
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
    Splits transcript into exact 10-second scenes (capped to max 60 scenes)
    and produces visually consistent prompts with toy car continuity and sound effects.
    Uses Gemini API if key is present, otherwise smart local director engine.
    """
    try:
        # Step 1: Chunk into 10s scenes (strictly max 60 scenes)
        raw_scenes = chunk_transcript_to_10s_scenes(
            transcript_items=req.transcript_items,
            total_duration_sec=req.duration,
            scene_duration=req.scene_duration,
            max_scenes=60
        )

        title = req.metadata.get("title", "")
        full_text = " ".join([s["dialogue"] for s in raw_scenes])
        vision = extract_kids_video_vision(title, full_text)

        anchors_dict = {
            "subject": req.custom_subject or "",
            "product": req.custom_product or "",
            "setting": req.custom_setting or "",
            "style": req.custom_style or ""
        }

        # Step 2: If Gemini API key is provided, request Gemini AI enhanced prompts for Kids video
        gemini_scenes = None
        engine_used = "Smart Local Kids Director Engine (Free / Offline)"
        if req.gemini_api_key and req.gemini_api_key.strip():
            gemini_scenes = generate_kids_prompts_with_gemini(
                scenes_data=raw_scenes,
                anchors=anchors_dict,
                video_meta=req.metadata,
                video_vision=vision["vision_summary"],
                language=req.language,
                api_key=req.gemini_api_key
            )
            if gemini_scenes:
                engine_used = "Google Gemini 1.5 Flash Vision AI"
        
        # Step 3: Generate and assemble consistent AI video generation prompts
        processed_scenes = generate_consistent_scene_prompts(
            scenes=raw_scenes,
            video_meta=req.metadata,
            language=req.language,
            custom_subject=req.custom_subject,
            custom_product=req.custom_product,
            custom_setting=req.custom_setting,
            custom_style=req.custom_style,
            image_context=req.image_context,
            gemini_scenes=gemini_scenes
        )
        
        anchors = processed_scenes[0]["anchors"] if processed_scenes else {}
        
        return {
            "status": "success",
            "total_scenes": len(processed_scenes),
            "max_scenes_limit": 60,
            "scene_duration_sec": req.scene_duration,
            "video_duration_sec": req.duration,
            "video_vision": vision,
            "engine_used": engine_used,
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
