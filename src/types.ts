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

export interface ExtractResponseData {
  metadata: VideoMetadata;
  language: string;
  method: string;
  items: TranscriptItem[];
  full_text: string;
  total_segments: number;
}

export interface SceneAnchors {
  subject: string;
  product: string;
  setting: string;
  style: string;
}

export interface ScenePromptItem {
  scene_index: number;
  time_range: string;
  start_time: number;
  end_time: number;
  duration_sec: number;
  dialogue: string;
  action_description: string;
  camera_directive: string;
  camera_purpose: string;
  video_prompt: string;
  negative_prompt: string;
  anchors: SceneAnchors;
}

export interface GenerateResponse {
  status: string;
  total_scenes: number;
  scene_duration_sec: number;
  video_duration_sec: number;
  anchors: SceneAnchors;
  scenes: ScenePromptItem[];
}

