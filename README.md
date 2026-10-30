# 🚗 imsy tools yt (v2.1)
> **Google Flow Edition: Kids YouTube Remake Engine didukung Model DeepSeek-V4.1-Flash (60 Scene Prompt AI Sinematik)**

**imsy tools yt** adalah aplikasi web modern berbasis **React TSX + FastAPI** yang dirancang khusus untuk membuat ulang (*remake*) konten **video YouTube anak-anak (lagi main mobil-mobilan, monster truck, Hot Wheels, balapan ceria, suara vroom-vroom/sound effects kartun)** ke format **60 scene prompt (10 detik per scene)** yang hidup, sinematik, dan konsisten.

---

## 🌟 Peningkatan Baru: Integrasi DeepSeek-V4.1-Flash & Prompt Sinematik Alami

1. **Integrasi Model DeepSeek-V4.1-Flash (`deepseek-ai/DeepSeek-V4.1-Flash-1017`)**
   - Mendukung model multimodal terbaru [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) melalui **Hugging Face Inference Router**.
   - Pengguna cukup memasukkan Token Hugging Face gratis (`hf_...`) dari [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
   - Juga mendukung **DeepSeek Official API** (`sk-...`) dan **Google Gemini 1.5 Flash Vision**.

2. **Prompt Tidak Lagi Kaku (No Stiff Brackets)**
   - Format kaku lama dengan pemisah kurung siku `[Objek: ...] | [Gaya: ...]` telah **dihapus sepenuhnya**!
   - Prompt kini diracik menjadi **kalimat deskriptif sinematik yang mengalir alami (*fluid cinematic sentences*)**, mencakup dinamika gerak mobil mainan, ekspresi tawa anak, manuver kamera sinematik, dan isyarat efek suara `[SFX: ...]`.
   - Format ini terbukti memberikan hasil render visual paling maksimal di generator video AI kelas atas seperti **Google Veo**, **Kling AI**, **Runway Gen-3**, **Luma Dream Machine**, dan **Sora**.

3. **Membaca Visi Cerita YouTube & Analisis Kata Kunci 10 Detik**
   - AI membaca transkrip audio per 10 detik dan mengenali kata kunci aksi secara langsung:
     - Jika audio menyebut *"jangan sampai tabrak"*, prompt otomatis menyusun aksi mobil oleng menabrak balok empuk dengan sound effect tabrakan lucu kartun.
     - Jika audio menyebut *"melompat tinggi"*, prompt menyusun aksi mobil melompat di tanjakan berputar 360 derajat di udara.
     - Jika audio menyebut *"kencang/balap"*, prompt menyusun adegan mobil memacu kecepatan di lintasan lurus dengan debu animasi kartun.

4. **Upload 1 Foto Mainan Mobil / Karakter ("Bisa Dilihat Tentang Apa")**
   - Cukup upload 1 foto mobil mainan atau karakter anak.
   - AI mengidentifikasi bentuk mobil, warna cat, dan ban off-road lalu menguncinya paten ke **seluruh 60 scene** (*no morphing*).

5. **Format 60 Scene Penuh (10 Detik per Scene)**
   - Menghasilkan alur storyboard tepat **60 scene prompt** (total 600 detik / 10 menit konten video padat per 10 detik).

6. **Deteksi Hardware Otomatis (GPU CUDA RTX 3050 & CPU)**
   - Akselerasi Whisper GPU NVIDIA RTX 3050 tanpa perlu instalasi ffmpeg manual.

---

## 🚀 Cara Menjalankan

Cukup klik dua kali file [`start.bat`](file:///d:/script/LINKYT2PROMPT/start.bat) atau lewat terminal:
```bash
python run.py
```
Aplikasi akan otomatis mendeteksi GPU Anda dan membuka browser di:
👉 **`http://127.0.0.1:8000`**

---

## 🛠️ Struktur Project

```
LINKYT2PROMPT/
├── dist/                   # Hasil build frontend siap saji
├── server/                 # Backend FastAPI
│   ├── hardware.py         # Deteksi GPU NVIDIA CUDA & CPU
│   ├── transcriber.py      # Ekstraksi YouTube Transcript & Whisper
│   ├── llm_service.py      # Integrasi DeepSeek-V4.1-Flash (Hugging Face) & DeepSeek API
│   ├── gemini_service.py   # Integrasi Google Gemini Vision
│   ├── prompt_engine.py    # Logika Alur Cerita Sinematik & 60 Scene
│   └── main.py             # FastAPI REST Server
├── src/                    # Frontend React TSX
│   ├── components/
│   │   ├── Header.tsx            # Navigasi & Status DeepSeek-V4.1
│   │   ├── HardwareBadge.tsx     # Status GPU / CPU
│   │   ├── LlmApiKeyModal.tsx    # Pengaturan Token DeepSeek-V4.1 / HF / Gemini
│   │   ├── UrlInputNode.tsx      # Node 01: Input YouTube & Visi Cerita
│   │   ├── ImageUploadNode.tsx   # Node 02: Upload 1 Foto Mainan Mobil
│   │   ├── ConsistencyNode.tsx   # Node 03: Konsistensi 60 Scene Video Anak
│   │   ├── TranscriptNode.tsx    # Node 04: Transkrip Percakapan YT
│   │   ├── SceneFlowNode.tsx     # Final Flow: Alur 60 Scene Sinematik
│   │   └── ExportModal.tsx       # Modal Ekspor Format Lengkap
│   ├── App.tsx             # Canvas Alur Google Flow
│   ├── types.ts            # Definisi TypeScript
│   └── index.css           # Styling Google Flow & Tailwind
├── run.py                  # Script Peluncur Otomatis
├── start.bat               # Windows Launcher
└── package.json            # Dependensi React & Vite
```
