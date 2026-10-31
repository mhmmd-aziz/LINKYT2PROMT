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
        extract_kids_video_vision,
        generate_youtube_viral_package
    )
    from server.llm_service import (
        verify_llm_key,
        generate_scenes_with_deepseek,
        detect_api_provider
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
        extract_kids_video_vision,
        generate_youtube_viral_package
    )
    from llm_service import (
        verify_llm_key,
        generate_scenes_with_deepseek,
        detect_api_provider
    )
    from gemini_service import (
        verify_gemini_key,
        analyze_uploaded_image,
        generate_kids_prompts_with_gemini
    )

app = FastAPI(
    title="imzy tools yt API",
    description="Backend for Kids YouTube Video Remake with DeepSeek-V4.1-Flash LLM Integration (Google Flow Style)",
    version="2.2.0"
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
    api_token: Optional[str] = Field(None, description="Optional Hugging Face or Gemini API token")
    gemini_api_key: Optional[str] = Field(None, description="Optional Gemini API key")

class VerifyKeyRequest(BaseModel):
    api_token: str = Field(..., description="DeepSeek, HuggingFace, or Gemini Token to verify")
    provider: Optional[str] = Field(None, description="Optional provider override")

class GenerateRequest(BaseModel):
    metadata: Dict[str, Any]
    transcript_items: List[Dict[str, Any]]
    duration: float
    scene_duration: float = 10.0
    language: str = "en"
    custom_subject: Optional[str] = None
    custom_product: Optional[str] = None
    custom_setting: Optional[str] = None
    custom_style: Optional[str] = None
    image_context: Optional[Dict[str, Any]] = None
    api_token: Optional[str] = None
    provider: Optional[str] = None

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "imzy tools yt", "llm_supported": ["DeepSeek-V4.1-Flash", "DeepSeek Official", "Gemini 1.5 Flash"]}

@app.get("/api/hardware")
def get_hardware_info():
    """Returns detected GPU (RTX 3050, CUDA, VRAM) and CPU details."""
    return get_system_hardware()

@app.post("/api/llm/verify")
def api_verify_llm(req: VerifyKeyRequest):
    """Checks validity of DeepSeek V4.1 Flash (Hugging Face), DeepSeek Official, or Gemini token."""
    res = verify_llm_key(req.api_token, provider=req.provider)
    return res

# Keep legacy endpoint for backwards compatibility
@app.post("/api/gemini/verify")
def api_verify_gemini_key(req: VerifyKeyRequest):
    res = verify_llm_key(req.api_token, provider="gemini")
    return res

@app.post("/api/analyze-image")
def api_analyze_image(req: AnalyzeImageRequest):
    """
    Analyzes 1 uploaded toy car / kids character / setting image.
    Uses AI Vision if API token provided, or smart local kids vision engine.
    """
    try:
        token = req.api_token or req.gemini_api_key
        analysis = analyze_uploaded_image(req.image_base64, api_key=token)
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
    Splits transcript into exact 10-second scenes (capped to max 20 scenes)
    and produces visually consistent, non-stiff fluid prompts with toy car continuity and full 10s English speech.
    Uses DeepSeek V4.1 Flash (Hugging Face) if provided, DeepSeek Official, Gemini, or smart local director.
    """
    try:
        # Step 1: Chunk into 10s scenes (strictly max 20 scenes)
        raw_scenes = chunk_transcript_to_10s_scenes(
            transcript_items=req.transcript_items,
            total_duration_sec=req.duration,
            scene_duration=req.scene_duration,
            max_scenes=20
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

        # If user uploaded an image photo, lock the product anchor from image analysis
        if req.image_context:
            rec_car = req.image_context.get("recommended_anchor_product") or req.image_context.get("product_name")
            if rec_car and not req.custom_product:
                anchors_dict["product"] = rec_car
            if req.image_context.get("recommended_anchor_subject") and not req.custom_subject:
                anchors_dict["subject"] = req.image_context.get("recommended_anchor_subject")
            if req.image_context.get("recommended_setting") and not req.custom_setting:
                anchors_dict["setting"] = req.image_context.get("recommended_setting")

        token = (req.api_token or "").strip()
        llm_scenes = None
        engine_used = "Smart Kids Director Engine (Dynamic Local Mode)"

        # Step 2: Route to DeepSeek V4.1 Flash, DeepSeek Official, or Gemini
        # Both models receive the full video title, transcript, and user's uploaded photo!
        if token:
            prov = req.provider or detect_api_provider(token)
            print(f"[Engine] Token terdeteksi ({prov}). Memulai request ke {prov}...")
            if prov in ("tokenharbor", "huggingface_deepseek", "deepseek_official"):
                llm_scenes = generate_scenes_with_deepseek(
                    scenes_data=raw_scenes,
                    anchors=anchors_dict,
                    video_meta=req.metadata,
                    video_vision=vision["vision_summary"],
                    language=req.language,
                    api_token=token,
                    provider=prov,
                    image_context=req.image_context,
                    full_transcript=full_text
                )
                if llm_scenes:
                    if prov == "tokenharbor":
                        engine_used = "DeepSeek-V4.1-Flash (Token Harbor AI)"
                    elif prov == "huggingface_deepseek":
                        engine_used = "DeepSeek-V4.1-Flash-1017 (Hugging Face AI)"
                    else:
                        engine_used = "DeepSeek Official AI"
                    print(f"[Engine] Berhasil! Alur 20-scene disusun langsung oleh {engine_used}!")
                else:
                    print(f"[Engine Fallback] DeepSeek ({prov}) gagal merespons atau token tidak valid. Beralih otomatis ke Smart Kids Director Engine.")
            elif prov == "gemini":
                llm_scenes = generate_kids_prompts_with_gemini(
                    scenes_data=raw_scenes,
                    anchors=anchors_dict,
                    video_meta=req.metadata,
                    video_vision=vision["vision_summary"],
                    language=req.language,
                    api_key=token,
                    image_context=req.image_context,
                    full_transcript=full_text
                )
                if llm_scenes:
                    engine_used = "Google Gemini 1.5 Flash Vision AI"
                    print(f"[Engine] Berhasil! Alur 20-scene disusun oleh Gemini Vision!")
                else:
                    print(f"[Engine Fallback] Gemini gagal merespons. Beralih otomatis ke Smart Kids Director Engine.")
        else:
            print("[Engine] Belum ada API Token LLM. Menggunakan Smart Kids Director Engine (Mode Dinamis Otomatis).")
        
        # Step 3: Generate and assemble fluid, cinematic AI video generation prompts
        processed_scenes = generate_consistent_scene_prompts(
            scenes=raw_scenes,
            video_meta=req.metadata,
            language=req.language,
            custom_subject=req.custom_subject,
            custom_product=req.custom_product,
            custom_setting=req.custom_setting,
            custom_style=req.custom_style,
            image_context=req.image_context,
            llm_scenes=llm_scenes
        )
        
        anchors = processed_scenes[0]["anchors"] if processed_scenes else {}
        
        # Step 4: Generate viral YouTube kit (Hype FYP Titles, SEO Description with timestamps, and AI Thumbnail Prompts for Gemini)
        youtube_package = generate_youtube_viral_package(
            video_meta=req.metadata,
            anchors=anchors,
            scenes=processed_scenes,
            image_context=req.image_context,
            vision=vision
        )

        return {
            "status": "success",
            "total_scenes": len(processed_scenes),
            "max_scenes_limit": 20,
            "scene_duration_sec": req.scene_duration,
            "video_duration_sec": req.duration,
            "video_vision": vision,
            "engine_used": engine_used,
            "anchors": anchors,
            "scenes": processed_scenes,
            "youtube_package": youtube_package
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal membuat alur prompt scene: {str(e)}")

class YouTubeKitRequest(BaseModel):
    metadata: Dict[str, Any]
    anchors: Dict[str, str]
    scenes: List[Dict[str, Any]] = []
    image_context: Optional[Dict[str, Any]] = None

@app.post("/api/youtube-kit")
async def get_youtube_kit(req: YouTubeKitRequest):
    """
    Independent endpoint to generate/refresh YouTube FYP titles, descriptions, and Gemini thumbnail prompts.
    """
    try:
        pkg = generate_youtube_viral_package(
            video_meta=req.metadata,
            anchors=req.anchors,
            scenes=req.scenes,
            image_context=req.image_context
        )
        return {"status": "success", "youtube_package": pkg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menghasilkan YouTube kit: {str(e)}")

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
