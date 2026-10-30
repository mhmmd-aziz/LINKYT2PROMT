# 🚗 imsy tools yt (v2.0)
> **Google Flow Edition: Alat Remake Video YouTube Anak (Main Mobil & Sound Effects) ke 60 Scene AI Video Prompt Konsisten**

**imsy tools yt** adalah aplikasi web modern berbasis **React TSX + FastAPI** yang dirancang khusus untuk kreator konten video anak-anak (Kids YouTube Channel, mainan mobil-mobilan, monster truck, Hot Wheels, balapan ceria, suara vroom-vroom/sound effects kartun). 

Aplikasi ini membaca video YouTube yang Anda copas link-nya, mengenali **visi cerita dan tema bermain mobil**, lalu menyusun ulang menjadi alur storyboard **60 scene prompt (10 detik per scene penuh)** yang bagus, konsisten, dan siap di-generate ke model AI video (Google Veo, Kling AI, Runway Gen-3, Luma Dream Machine).

---

## 🌟 Fitur Utama imsy tools yt

1. **Mengenali Visi Video YouTube yang Di-paste**
   - Cukup copas link video YouTube anak (misalnya video orang lain yang lagi main mobil-mobilan, monster truck, balapan di track, dsb).
   - Sistem secara otomatis menganalisis judul dan transkrip audio untuk membaca **Visi & Tema Cerita** (misal: *Petualangan Truk Monster Melompati Rintangan, Balapan Mobil Cepat di Sirkuit, Misi Penyelamatan Mobil Kota Ceria*).

2. **Upload 1 Foto Mainan Mobil / Karakter ("Bisa Dilihat Tentang Apa")**
   - Upload 1 foto mobil mainan atau karakter anak yang Anda miliki.
   - AI Vision menganalisis detail mobil (model, warna mencolok seperti merah-kuning, ban besar off-road, nomor, bodi 3D animasi).
   - **Kunci Otomatis**: Ciri mobil mainan dan anak ini dikunci paten dari Scene 1 sampai Scene 60 agar model AI video tidak berubah bentuk (*no morphing*).

3. **Versi 60 Scene Penuh (10 Detik per Scene)**
   - Menyusun alur cerita video anak ke versi **maksimal 60 scene prompt** (total 600 detik / 10 menit konten video padat).
   - Setiap scene berisi tepat 10 detik aksi main mobil yang menyenangkan.

4. **Sound Effects Ceria (SFX) di Setiap Scene**
   - Mengintegrasikan efek suara khas video anak-anak di setiap scene prompt:
     - `[SFX: Vroom vroom mesin mobil menderu ceria, decitan ban 'squeak!', tawa riang anak]`
     - `[SFX: Klakson tin-tin lucu 'beep beep!', musik ceria bertempo riang]`
     - `[SFX: Efek lompatan kartun 'boing boing!', desingan angin 'wuuush!', sorak 'Horeee!']`
     - `[SFX: Tabrakan lembut balok susun, selebrasi kembang api kartun, tepuk tangan]`

5. **Dual Engine: Google Gemini 1.5 Flash Vision AI + Smart Local Kids Director**
   - **Google Gemini API**: Menggunakan model vision multimodal untuk meracik prompt video sinematik 3D Pixar/Disney style yang sangat hidup.
   - **Smart Local Kids Director**: Berjalan 100% offline, lokal, dan gratis tanpa butuh API key jika Anda ingin langsung pakai.

6. **Deteksi Hardware Otomatis (GPU CUDA RTX 3050 & CPU)**
   - Mendeteksi otomatis GPU NVIDIA CUDA RTX 3050 Laptop GPU Anda untuk akselerasi transkripsi Whisper tanpa butuh instalasi ffmpeg tambahan.

7. **Export 1-Klik Siap Render**
   - Salin prompt per scene.
   - Export Semua Prompt Sekaligus, Download JSON, Download CSV / Spreadsheet, dan Subtitle (.SRT).

---

## 🚀 Cara Menjalankan

Cukup klik dua kali file [`start.bat`](file:///d:/script/LINKYT2PROMPT/start.bat) atau lewat terminal:
```bash
python run.py
```
Aplikasi akan otomatis mendeteksi GPU Anda dan membuka browser di `http://127.0.0.1:8000`.

---

## 🛠️ Struktur Project

```
LINKYT2PROMPT/
├── dist/                   # Hasil build frontend siap saji
├── server/                 # Backend FastAPI
│   ├── hardware.py         # Deteksi GPU NVIDIA CUDA & CPU
│   ├── transcriber.py      # Ekstraksi YouTube Transcript & Whisper
│   ├── gemini_service.py   # Integrasi Google Gemini Vision & Kids Video AI
│   ├── prompt_engine.py    # Logika Kids Video, Visi Cerita & 60 Scene
│   └── main.py             # FastAPI REST Server & Static File Host
├── src/                    # Frontend React TSX
│   ├── components/
│   │   ├── Header.tsx            # Navigasi & Branding imsy tools yt
│   │   ├── HardwareBadge.tsx     # Status GPU / CPU
│   │   ├── GeminiApiKeyModal.tsx # Pengaturan Gemini API Key & Mesin AI
│   │   ├── UrlInputNode.tsx      # Node 01: Input YouTube & Visi Cerita
│   │   ├── ImageUploadNode.tsx   # Node 02: Upload 1 Foto Mainan Mobil
│   │   ├── ConsistencyNode.tsx   # Node 03: Konsistensi 60 Scene Video Anak
│   │   ├── TranscriptNode.tsx    # Node 04: Transkrip Percakapan YT
│   │   ├── SceneFlowNode.tsx     # Final Flow: Alur 60 Scene + Sound Effects
│   │   └── ExportModal.tsx       # Modal Ekspor Format Lengkap
│   ├── App.tsx             # Canvas Alur Google Flow
│   ├── types.ts            # Definisi TypeScript
│   └── index.css           # Styling Google Flow & Tailwind
├── run.py                  # Script Peluncur Otomatis
├── start.bat               # Windows Launcher
└── package.json            # Dependensi React & Vite
```
