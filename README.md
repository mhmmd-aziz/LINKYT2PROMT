# ⚡ imzy affilate (v1.1)
> **Google Flow Edition: Alat Ekstraksi Transkrip YouTube ke Prompt Video AI Konsisten (10 Detik Penuh per Scene - Max 60 Scenes)**

Aplikasi web modern berbasis **React TSX + FastAPI** yang dirancang persis dengan visual alur **Google Flow / Google AI Studio**. Membantu kreator konten & affiliate marketer mengubah link YouTube + foto produk menjadi alur storyboard prompt teks-ke-video (untuk Google Veo, Kling AI, Runway Gen-3, Luma Dream Machine) dengan konsistensi objek dan tokoh 100%.

---

## 🌟 Fitur Baru & Peningkatan Utama

1. **Modal Copas Link YouTube (Anti-Error)**
   - Mendukung YouTube reguler, Shorts, atau Video ID.
   - Menggunakan `youtube-transcript-api` (kompatibel penuh v1.2+) dengan fallback GPU **Faster-Whisper** langsung via stream PyAV tanpa butuh instalasi eksternal `ffmpeg.exe`!

2. **Upload 1 Foto Produk / Objek Konsisten ("Bisa Dilihat Tentang Apa")**
   - Mendukung upload 1 foto produk affiliasi, kemasan, atau karakter.
   - **Analisis Visual Cerdas**: Sistem langsung menganalisis foto tersebut untuk menampilkan:
     - Nama Produk / Objek
     - Kategori & Ciri Khas Visual
     - Teks / Merek yang Terdeteksi
     - Rekomendasi Anchor Objek & Subjek
   - 1-Klik Kunci: Menempelkan deskripsi visual foto ke semua scene prompt secara konsisten.

3. **Per Scene 10 Detik Penuh & Maksimal 60 Scene Prompt**
   - Setiap scene berisi tepat **10 detik penuh percakapan audio**.
   - Dibatasi secara optimal **maksimal 60 scene prompt** (setara 10 menit konten video padat per 10s) agar alur terstruktur rapi dan terhindar dari pemborosan kuota render video AI.

4. **Mesin AI: Google Gemini 1.5 Flash + Smart Local Engine**
   - **Bagaimana prompt dihasilkan?**
     - **Dengan Gemini API Key**: Menggunakan model multimodal **Google Gemini 1.5 Flash Vision**. Membaca foto yang di-upload + transkrip 10 detik untuk menyusun prompt sinematik level sutradara profesional.
     - **Tanpa API Key (Smart Local Engine)**: Berjalan 100% lokal, cepat, dan gratis menggunakan algoritma storyboard sinematik dan rotasi kamera dinamis (Establishing Shot ➔ Medium Close-up ➔ Macro Product ➔ Over-the-shoulder ➔ Call to Action).
   - Menu pengaturan API Key di Header untuk memasukkan dan menguji Google Gemini API Key secara aman.

5. **Konsistensi Objek & Tokoh Antar Scene (Google Flow Matrix)**
   - Mengunci objek produk dan ciri subjek (wajah, busana, ekspresi) dari Scene 1 sampai Scene terakhir agar model AI video tidak berubah bentuk (*no morphing*).

6. **Deteksi Hardware Otomatis (GPU CUDA RTX 3050 & CPU)**
   - Otomatis mendeteksi kartu grafis sistem Anda (**NVIDIA GeForce RTX 3050 Laptop GPU 4GB VRAM - CUDA 12.1**).
   - Mengatur path DLL PyTorch secara dinamis sehingga Whisper GPU berjalan lancar.

7. **Export Lengkap Siap Pakai**
   - 1-Klik Salin Prompt per scene.
   - Export Semua Prompt, Download JSON, Download CSV / Sheet, dan Subtitle (.SRT).

---

## 🚀 Cara Menjalankan

Cukup jalankan file `start.bat` dengan klik dua kali, atau lewat terminal:
```bash
python run.py
```
Aplikasi akan otomatis mendeteksi hardware GPU Anda dan membuka browser di `http://127.0.0.1:8000`.

---

## 🛠️ Struktur Project

```
LINKYT2PROMPT/
├── dist/                   # Hasil build frontend siap saji
├── server/                 # Backend FastAPI
│   ├── hardware.py         # Deteksi GPU NVIDIA CUDA & CPU
│   ├── transcriber.py      # Ekstraksi YouTube Transcript & Whisper (PyAV stream)
│   ├── gemini_service.py   # Integrasi Google Gemini Vision & Prompt AI
│   ├── prompt_engine.py    # Logika Scene 10s, Max 60 Scenes & Konsistensi
│   └── main.py             # FastAPI REST Endpoints & File Server
├── src/                    # Frontend React TSX
│   ├── components/
│   │   ├── Header.tsx            # Navigasi, Badge Hardware & Status AI
│   │   ├── HardwareBadge.tsx     # Modal Status GPU / CPU
│   │   ├── GeminiApiKeyModal.tsx # Pengaturan Gemini API Key & Mesin AI
│   │   ├── UrlInputNode.tsx      # Node 01: Input YouTube Link
│   │   ├── ImageUploadNode.tsx   # Node 02: Upload 1 Foto & Analisis Visual
│   │   ├── ConsistencyNode.tsx   # Node 03: Kunci Konsistensi 10s (Max 60 Scenes)
│   │   ├── TranscriptNode.tsx    # Node 04: Transkrip Percakapan YT
│   │   ├── SceneFlowNode.tsx     # Final Flow: Alur Prompt-to-Video
│   │   └── ExportModal.tsx       # Modal Ekspor Format Lengkap
│   ├── App.tsx             # Canvas Alur Google Flow
│   ├── types.ts            # Definisi TypeScript
│   └── index.css           # Styling Google Flow & Tailwind
├── run.py                  # Script Peluncur Otomatis Satu Perintah
├── start.bat               # Windows Launcher
└── package.json            # Dependensi React & Vite
```
