export interface GpuDetails {
  available: boolean;
  device_name?: string;
  device_count?: number;
  total_vram_mb?: number;
  total_vram_gb?: number;
  allocated_vram_mb?: number;
  reserved_vram_mb?: number;
  cuda_version?: string;
  compute_capability?: [number, number];
  status: string;
  error?: string;
}

export interface CpuDetails {
  processor: string;
  cpu_count_logical: number;
  cpu_count_physical: number;
  cpu_percent: number;
  ram_total_gb: number;
  ram_available_gb: number;
  ram_percent: number;
}

export interface HardwareInfo {
  gpu: GpuDetails;
  cpu: CpuDetails;
  recommended_device: 'cuda' | 'cpu';
  system: string;
  platform: string;
}

export interface VideoMetadata {
  id: string;
  url: string;
  title: string;
  duration: number;
  author: string;
  thumbnail: string;
  description: string;
}

export interface TranscriptItem {
  start: number;
  duration: number;
  end: number;
  text: string;
}

export interface KidsVideoVision {
  vision_theme: string;
  vision_summary: string;
  default_car: string;
  default_arena: string;
}

export interface ExtractResponseData {
  metadata: VideoMetadata;
  language: string;
  method: string;
  items: TranscriptItem[];
  full_text: string;
  total_segments: number;
  video_vision?: KidsVideoVision;
}

export interface SceneAnchors {
  subject: string;
  product: string;
  setting: string;
  style: string;
}

export interface ImageAnalysisResult {
  product_name: string;
  category: string;
  visual_description: string;
  recommended_anchor_product: string;
  recommended_anchor_subject: string;
  recommended_setting: string;
  detected_text?: string;
  source?: string;
}

export interface ScenePromptItem {
  scene_index: number;
  time_range: string;
  start_time: number;
  end_time: number;
  duration_sec: number;
  dialogue: string;
  english_dialogue?: string;
  word_count?: number;
  speech_duration_est?: string;
  act?: string;
  milestone?: string;
  story_link?: string;
  sound_effects?: string;
  visual_effects?: string;
  is_closing?: boolean;
  action_description: string;
  camera_directive: string;
  camera_purpose: string;
  video_prompt: string;
  negative_prompt: string;
  anchors: SceneAnchors;
}

export interface YouTubePackage {
  viral_titles: string[];
  primary_title: string;
  description: string;
  tags: string[];
  hashtags: string[];
  thumbnail_prompt: string;
  thumbnail_alt_prompt?: string;
  thumbnail_text?: string;
  thumbnail_text_options?: string[];
  thumbnail_composition_tips: string;
}

export interface GenerateResponse {
  status: string;
  total_scenes: number;
  max_scenes_limit: number;
  scene_duration_sec: number;
  video_duration_sec: number;
  video_vision?: KidsVideoVision;
  engine_used: string;
  anchors: SceneAnchors;
  scenes: ScenePromptItem[];
  youtube_package?: YouTubePackage;
}
